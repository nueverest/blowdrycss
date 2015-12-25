__author__ = 'chad nelson'
__project__ = 'blow dry css'


class ResponsiveParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    **Generic Screen Size Triggers:**

    - ``'inline-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit
      for ``medium`` size screens.

    **Custom Usage: Set a specific pixel limit.**

    - ``'block-480px-down'`` -- Only displays the HTML element as a block for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.

        - **Note:** If unit conversion is enabled i.e. ``px_to_em`` is ``True``, then 624px would be converted to 39em.

    **Responsive Flag:**

    Append ``'-r'`` to the end of an encoded property values to scale the value up and down based on screen size.

    Note: This only works on property values containing distance--based units (pixels, em, etc).

    - General format: ``<name>-<value>-r``

    - Specific case: ``font-size-24-r``

    - Priority ``!important`` case: ``font-size-24-r-i``

        - (``'-i'`` *is always last*)

    **Responsive Scaling Ratios:**

    - Assuming ``font-size-24-r`` is the encoded css class, the font-size will respond to the screen size according
      to the following table:

        +-------------+---------------+----------------+------+-------+
        | Screen Size | Trigger Range | Scaling Factor |  px  | em    |
        +-------------+---------------+----------------+------+-------+
        | Large       |    > 720px    |        1       |  24  | 1.5   |
        +-------------+---------------+----------------+------+-------+
        | Medium      |    < 720px    |      1.125     | 21.3 | 1.333 |
        +-------------+---------------+----------------+------+-------+
        | Small       |    < 480px    |      1.25      | 19.2 | 1.2   |
        +-------------+---------------+----------------+------+-------+

    - Generated CSS for ``font-size-24-r``::

        .font-size-24-r {
            font-size: 24px;

            // medium screen font size reduction
            @media only screen and (max-width: 720px) {
                font-size: 21.3px;
            }

            // small screen font size reduction
            @media only screen and (max-width: 480px) {
                font-size: 19.2px;
            }
        }

    :type css_class: str
    :type px_to_em: bool

    :param css_class: Potentially encoded css class that may or may not be parsable.
    :param px_to_em: A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion.
        False disables unit conversions meaning any pixel value remains unchanged.
    :return: None

    **Examples:**

    >>> 'WARNING: NOT IMPLEMENTED YET'

    """

    def __init__(self, css_class='', px_to_em=True):
        # Default Screen Width Settings
        # Tuple Format (Lower Limit, Upper Limit) in pixels.
        # Note: These values do not change even if unit conversion is enabled i.e. ``px_to_em`` is ``True``.
        # Common Screen Resolutions: https://en.wikipedia.org/wiki/List_of_common_resolutions
        self.xxsmall = (0, 120)
        self.xsmall = (121, 240)
        self.small = (241, 480)
        self.medium = (481, 720)            # Typical mobile device crossover point @ 720px.
        self.large = (721, 1024)
        self.xlarge = (1025, 1366)
        self.xxlarge = (1367, 1920)
        self.giant = (1921, 2560)
        self.xgiant = (2561, 10**100)

        self.size_ranges_dict = {
            'xxsmall': self.xxsmall,
            'xsmall': self.xxsmall,
            'small': self.small,
            'medium': self.medium,
            'large': self.large,
            'xlarge': self.xlarge,
            'xxlarge': self.xxlarge,
            'giant': self.giant,
            'xgiant': self.xgiant,
        }

        self.direction_set = {'-only', '-down', '-up', }

        self.responsive = '-r'

    # Media Query
#     @mixin text($font-color, $font-size, $font-family:"Open Sans", $line-height:inherit, $responsive:true) {
# 	color: $font-color;
# 	font-size: $font-size;
# 	font-family: $font-family, $default-font-family;
# 	line-height: $line-height;
#
# 	// Responsive font reduction
# 	@if $responsive {
# 		// medium screen font size reduction
# 		@media only screen and (max-width: $medium-width) {
# 			font-size: $font-size/$medium-reduction;
# 			line-height: $line-height/$medium-reduction;
# 		}
#
# 		// small screen font size reduction
# 		@media only screen and (max-width: $small-width) {
# 			font-size: $font-size/$small-reduction;
# 			line-height: $line-height/$small-reduction;
# 		}
# 	}
# }
#
# @mixin link($color, $hcolor, $size, $font-family:"Open Sans", $line-height:inherit, $deco1:none, $deco2:none, $responsive:true) {
# 	a {
# 		color: $color;
# 		font-size: $size;
# 		font-family: $font-family, $default-font-family;
# 		line-height: $line-height;
# 		text-decoration: $deco1;
# 		&:hover {
# 			color: $hcolor;
# 			text-decoration: $deco2;
# 		}
# 	}
#
# 	// Responsive font reduction
# 	@if $responsive {
# 		// medium screen font size reduction
# 		@media only screen and (max-width: $medium-width) {
# 			a {
# 				color: $color;
# 				font-size: $size/$medium-reduction;
# 				font-family: $font-family, $default-font-family;
# 				line-height: $line-height/$medium-reduction;
# 				text-decoration: $deco1;
#
# 				&:hover {
# 					color: $hcolor;
# 					text-decoration: $deco2;
# 				}
# 			}
# 		}
#
# 		// small screen font size reduction
# 		@media only screen and (max-width: $small-width) {
# 			a {
# 				color: $color;
# 				font-size: $size/$small-reduction;
# 				font-family: $font-family, $default-font-family;
# 				line-height: $line-height/$small-reduction;
# 				text-decoration: $deco1;
#
# 				&:hover {
# 					color: $hcolor;
# 					text-decoration: $deco2;
# 				}
# 			}
# 		}
# 	}
# }
