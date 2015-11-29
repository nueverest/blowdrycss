from string import digits
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class UnitParser(object):
    def __init__(self, base=16, px_to_em=True):
        self.base = float(base)        # 16px = 1em
        self.px_to_em = px_to_em
        self.allowed = set(digits + '-.px')

        # Reference: http://www.w3.org/TR/CSS21/propidx.html
        # Extracted all properties containing Values of <angle>, <percentage>, <length>, <time>, <frequency>
        # IDEA: Build webscraper that auto-extracts these.\
        self.default_property_units_dict = {       # Possible Occurrences:
            'azimuth': 'deg',                 # single
            'background-position': '%',       # single or double

            # 'border': 'px',                 # single   Shorthand Property unit addition Not implemented
            'border-top': 'px',               # single
            'border-right': 'px',             # single
            'border-bottom': 'px',            # single
            'border-left': 'px',              # single
            'border-spacing': 'px',           # single

            'border-width': 'px',             # single
            'border-top-width': 'px',         # single
            'border-right-width': 'px',       # single
            'border-bottom-width': 'px',      # single
            'border-left-width': 'px',        # single

            'elevation': 'deg',               # single

            # 'font': 'px',                   # single    Shorthand Property unit addition Not implemented
            'font-size': 'px',                # single

            'height': 'px',                   # single
            'max-height': 'px',               # single
            'min-height': 'px',               # single

            'letter-spacing': 'px',           # single
            'word-spacing': 'px',             # single

            'line-height': 'px',              # single

            'top': 'px',                      # single
            'right': 'px',                    # single
            'bottom': 'px',                   # single
            'left': 'px',                     # single

            'margin': 'px',                   # single, double, quadruple
            'margin-top': 'px',               # single
            'margin-right': 'px',             # single
            'margin-bottom': 'px',            # single
            'margin-left': 'px',              # single

            # 'outline': 'px',                # single    Shorthand Property unit addition Not implemented
            'outline-width': 'px',            # single

            'padding': 'px',                  # single, double, quadruple
            'padding-top': 'px',              # single
            'padding-right': 'px',            # single
            'padding-bottom': 'px',           # single
            'padding-left': 'px',             # single

            'pause': 'ms',                    # single, double
            'pause-after': 'ms',              # single
            'pause-before': 'ms',             # single

            'pitch': 'Hz',                    # single

            'text-indent': 'px',              # single

            'vertical-align': '%',            # single

            'volume': '%',                    # single

            'width': 'px',                    # single
            'max-width': 'px',                # single
            'min-width': 'px',                # single
        }

    # For property_name's that require units apply the default units defined in default_property_units_dict.
    # Handles cases input like: '12', '1 2 1 2', '5px 1 2px 13'
    # Unconverted Outputs: '12px', '1px 2px 1px 2px', '5px 1px 2px 13px'
    # 'em' Converted Outputs: '0.75em', '0.0625em 0.125em 0.0625em 0.125em', '0.3125em 0.0625em 0.125em 0.8125em'
    # 'px' is converted to 'em' if px_to_em is True.
    # Invalid input like '12a', '55zp', '42u3' are passed through and ignored.
    def add_units(self, property_name='', property_value=''):
        new_value = []
        try:
            default_units = self.default_property_units_dict[property_name]         # See if property_name has units.
            for val in property_value.split():                                      # single, double and quadruple
                if set(val) <= self.allowed:
                    val = val.replace('px', '')                                     # Handle pre-defined units casep
                    if self.px_to_em and default_units == 'px':                     # Convert units if required.
                        val = self.convert_px_to_em(pixels=val)
                        new_units = 'em'
                        new_value.append(val + new_units)
                    else:
                        new_value.append(val + default_units)                       # Use default units.
                else:                                                               
                    new_value.append(val)                                           # Pass through and ignore value.
            property_value = ' '.join(new_value)                                    # Put the new values back together.
        except KeyError:
            pass                                                                    # Property is unitless.        
        return property_value

    # Convert value from px to em using self.base.
    # Round float to 4 decimal places.
    def convert_px_to_em(self, pixels):
        em = float(pixels) / float(self.base)
        em = round(em, 4)
        return str(em)

