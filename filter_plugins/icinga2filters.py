import re

icinga2_keywords = [
  'NodeName',
  'ZoneName',
  'ConfigDir',
  'DataDir',
  'LogDir',
  'CacheDir',
  'SpoolDir',
  'InitRunDir',
  'ZonesDir',
  'PluginContribDir',
  'OK',
  'Warning',
  'Critical',
  'Unknown',
  'Up',
  'Down',
  'Problem',
  'Acknowledgement',
  'Recovery',
  'Custom',
  'FlappingStart',
  'FlappingEnd',
  'DowntimeStart',
  'DowntimeEnd',
  'DowntimeRemoved',
]

def check_keywords(value, iterator=None):
  """
  Quotes values that do not represent icinga2 keywords or match
  specific types or patterns, such as those representing host variables.
  Also leaves values unquoted that have appeared as keys or values in loops.

  Finally, values that are prefixed with "v'" will be return unquoted. That
  is probably a better trade-off than to just assume some strings –
  such as "name" – to always represent variables.
  """
  if type(value) is int:
    return value

  if type(iterator) is dict and (value == iterator['key'] or value == iterator['value']):
    return value

  pattern = re.compile(r'^(?:\d+(ms|s|m|h|d)?|host\.vars.*)$')
  if value in icinga2_keywords or pattern.match(value):
    return value

  pattern = re.compile(r'^v\'(.*)$')
  if pattern.match(value):
    return pattern.sub(r'\1', value)

  return '"{}"'.format(value)


def check_key_format(key, prefix):
  """
  Check if a key needs quoting or prefixing.
  E.g. attributes in CheckCommands that are actually flags ("--foo")
  require to be quoted.
  Also: Identifiers may not contain certain characters (e.g. space)
  or start with certain characters (e.g. digits).
  """
  if prefix:
    return prefix + key

  # pattern1 = re.compile(r'^\d')
  # pattern2 = re.compile(r'[\. ]+')
  # if key[:1] == '-' or pattern1.match(key) or pattern2.match(key):
  pattern = re.compile(r'^\d+.*|.*[\. ]+.*')
  if key[:1] == '-' or pattern.match(key):
    return '"{}"'.format(key)

  return key


class FilterModule(object):
  """
  custom jinja2 filters for working with icinga2
  """

  def filters(self):
    return {
      'icinga_vars': check_keywords,
      'icingakey': check_key_format,
    }
