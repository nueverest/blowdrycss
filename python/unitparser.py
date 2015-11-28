from string import digits
# custom
from datalibrary import default_property_units_dict
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class UnitParser(object):
    def __init__(self, base=16, px2em=True):
        self.base = int(base)        # 16px = 1em
        self.px2em = px2em
        self.allowed = set(digits + '-.')

    # For property_name's that require units apply the default units defined in default_property_units_dict.
    # Handles cases input like: '12', '35 15', '1 2 1 2'
    # Outputs: '12px', '35% 15%', '1px 2px 1px 2px'
    # Invalid input like '12a', '55zp', '42u3' raise a ValueError.
    def add_units(self, property_name='', property_value=''):
        new_value = []
        try:
            default_units = default_property_units_dict[property_name]              # See if property_name has units.
            for val in property_value.split():                                      # Double and quadruple values.
                if set(val) <= self.allowed:                                        # If value is missing units.
                    new_value.append(val + default_units)                           # Add default units.
                else:
                    new_value.append(val)                                           # Leave current value unchanged
            property_value = ' '.join(new_value)                                    # Put the new values back together
        except KeyError:
            pass                                                                    # Property does not need units.
        except ValueError:
            pass                                                                    # Invalid value.
        return property_value

    # Convert value from px to em using self.base.
    # Python will automatically round to 4 decimal places.
    def px_to_em(self, pixels):
        return int(pixels) / int(self.base)
