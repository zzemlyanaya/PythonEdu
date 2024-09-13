import os

path_of_the_directory = '/Users/zzemlyanaya/StudioProjects/skb-bank/core/uikit/src/main/kotlin/ru/skblab/compose/icons/common'

import1 = 'import androidx.compose.foundation.Image\nimport androidx.compose.material.icons.Icons\nimport androidx.compose.runtime.Composable\n'

import2 = 'import androidx.compose.ui.tooling.preview.Preview\n'
import3 = 'import ru.skblab.compose.icons.Lab\n'


def get_preview(name):
    return '\n\n@Preview\n@Composable\nprivate fun {0}Preview() {{\n\tImage(Icons.Lab.{1}, null)\n}}\n'.format(name,
                                                                                                               name)


icons = []
for filename in os.listdir(path_of_the_directory)[1:]:
    f = os.path.join(path_of_the_directory, filename)
    if not os.path.isfile(f) or not filename.endswith('.kt'):
        continue

    icons.append('LabIcons.' + filename.replace('.kt', ''))
    icons.sort()

    # lines = []
    # with open(f, 'r+') as file:
    #     lines = file.readlines()
    #
    # private_val = lines[-1]
    #
    # lines[2] = import1 + lines[2]
    # lines[9] += import2
    # lines[10] += import3
    # lines[11] += get_preview(icon_name) + private_val
    #
    # lines[26] = lines[26].replace('public', '')
    #
    # with open(f, 'w') as file:
    #     file.write(''.join(lines))
    #
    # lines.clear()
print(', '.join(icons))
