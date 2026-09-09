"""Read and validate the single academic record before generating either output."""
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
import hashlib
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'vendor'))
import yaml


class ContentError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    """Catch accidental duplicate sections instead of silently discarding entries."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ContentError(f'Duplicate field {key!r} near line {key_node.start_mark.line + 2}.')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def required_text(item, key, context):
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContentError(f'{context}.{key}: provide nonempty text.')
    return value


def records(value, context):
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ContentError(f'{context}: use a list of entries (or [] for an empty list).')
    return value


def check_link(value, context, root, local=True, pdf=False):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ContentError(f'{context}: provide a URL or omit the field.')
    parsed = urlsplit(value)
    if parsed.scheme in ('https', 'http') and parsed.netloc:
        return
    if not local or not value.startswith('/') or value.startswith('//') or parsed.scheme or parsed.netloc:
        expected = 'an https:// URL or a site path such as /papers/paper.pdf' if local else 'a full https:// or http:// URL'
        raise ContentError(f'{context}: use {expected}; do not use a Windows path.')
    path = unquote(parsed.path)
    if '\\' in path or ':' in path or any(part in ('.', '..', '') for part in path[1:].split('/')):
        raise ContentError(f'{context}: invalid local path {value!r}.')
    public = (root / 'public').resolve()
    parts = PurePosixPath(path).parts[1:]
    target = public.joinpath(*parts)
    if not target.resolve().is_relative_to(public) or not target.is_file():
        raise ContentError(f'{context}: local file is missing or outside public/: {path}.')
    # Windows accepts the wrong case locally, but public hosting may not.
    current = public
    for part in parts:
        if part not in {entry.name for entry in current.iterdir()}:
            raise ContentError(f'{context}: filename capitalization must match exactly: {path}.')
        current /= part
    if pdf:
        with target.open('rb') as handle:
            if target.suffix.lower() != '.pdf' or handle.read(5) != b'%PDF-':
                raise ContentError(f'{context}: expected a PDF file: {path}.')


def validate(data, root):
    if not isinstance(data, dict):
        raise ContentError('The front matter must contain named sections.')
    for link in records(data.setdefault('social_links', []), 'social_links'):
        required_text(link, 'label', 'social_links')
        check_link(link.get('url'), 'social_links.url', root, local=False)
    ids = set()
    for section in ('publications', 'other_publications'):
        for paper in records(data.get(section), section):
            paper_id = required_text(paper, 'id', section)
            context = f'{section}[{paper_id}]'
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', paper_id) or paper_id in ids:
                raise ContentError(f'{context}: IDs must be unique lowercase words/numbers separated by hyphens.')
            ids.add(paper_id)
            required_text(paper, 'title', context)
            if section == 'publications' and paper.get('type') not in ('published', 'working'):
                raise ContentError(f'{context}.type: use published or working.')
            for field in ('url', 'pdf', 'appendix'):
                if field in paper:
                    check_link(paper[field], f'{context}.{field}', root, local=field != 'url', pdf=field != 'url')
            for media in records(paper.get('media', []), f'{context}.media'):
                required_text(media, 'label', f'{context}.media')
                required_text(media, 'date', f'{context}.media')
                check_link(media.get('url'), f'{context}.media.url', root, local=False)
    homepage = data.setdefault('homepage', {})
    if not isinstance(homepage, dict) or set(homepage) - {'publications', 'working_papers'}:
        raise ContentError('homepage: use publications and working_papers lists of paper IDs.')
    for key, paper_type in [('publications', 'published'), ('working_papers', 'working')]:
        eligible = {paper['id'] for paper in data['publications'] if paper['type'] == paper_type}
        selected = homepage.setdefault(key, [paper['id'] for paper in data['publications'] if paper['type'] == paper_type][:2])
        if not isinstance(selected, list) or any(not isinstance(item, str) for item in selected):
            raise ContentError(f'homepage.{key}: use a list of paper IDs, or [] to hide the section.')
        if len(selected) > 2 or len(selected) != len(set(selected)):
            raise ContentError(f'homepage.{key}: select at most two different papers.')
        for paper_id in selected:
            if paper_id not in eligible:
                raise ContentError(f'homepage.{key}: {paper_id!r} must refer to a {paper_type} paper; update the homepage selection if its status changed.')
    for item in records(data.get('presentations', []), 'presentations'):
        if item.get('paper_id') not in {p['id'] for p in data['publications']}:
            raise ContentError(f'presentations: unknown paper_id {item.get("paper_id")!r}.')
    courses = records(data.setdefault('course_links', []), 'course_links')
    course_ids = set()
    for course in courses:
        course_id = required_text(course, 'id', 'course_links')
        context = f'course_links[{course_id}]'
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', course_id) or course_id in course_ids:
            raise ContentError(f'{context}: IDs must be unique lowercase words/numbers separated by hyphens.')
        course_ids.add(course_id)
        for key in ('code', 'title', 'term'):
            required_text(course, key, context)
        check_link(course.get('url'), f'{context}.url', root, local=False)
    datasets = records(data.setdefault('datasets', []), 'datasets')
    dataset_ids = set()
    for item in datasets:
        dataset_id = required_text(item, 'id', 'datasets')
        context = f'datasets[{dataset_id}]'
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', dataset_id) or dataset_id in dataset_ids:
            raise ContentError(f'{context}: IDs must be unique lowercase words/numbers separated by hyphens.')
        dataset_ids.add(dataset_id)
        if item.get('paper_id') not in ids:
            raise ContentError(f'{context}.paper_id: does not match a paper ID.')
        for key in ('title', 'description'):
            required_text(item, key, context)
        for key in ('updated', 'citation'):
            if key in item:
                required_text(item, key, context)
        files = records(item.get('files', []), f'{context}.files')
        for file in files:
            required_text(file, 'label', f'{context}.files')
            check_link(file.get('url'), f'{context}.files.url', root)
        if 'replication_url' in item:
            check_link(item['replication_url'], f'{context}.replication_url', root)
        if not files and not item.get('replication_url'):
            raise ContentError(f'{context}: add at least one file or replication_url, or leave this draft out of datasets.')
    return data


def load_content(source, root):
    raw = source.read_text(encoding='utf-8-sig')
    match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)(.*)\Z', raw, re.DOTALL)
    if not match:
        raise ContentError('Start academic.md with --- and close the YAML section with --- on its own line.')
    try:
        data = yaml.load(match[1], Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise ContentError(f'Invalid YAML in academic.md. Check indentation and quote text containing colons.\n{error}') from error
    validate(data, root)
    data['biography'] = match[2].strip()
    data['sourceHash'] = hashlib.sha256(raw.encode()).hexdigest()
    return data
