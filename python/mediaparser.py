__author__ = 'chad nelson'
__project__ = 'blow dry css'


class MediaParser(object):
    """ Enables powerful responsive @media query generation via screen size suffixes.

    Both of these are outside of the scope of the media parser. They belong in the ``datalibrary`` module.
    TODO: Consider the word ``show`` as shorthand for ``display-inline``.
    TODO: Consider the word ``hide`` as shorthand for ``display-none``.

    **General Usage:**

    - ``'display-small-only'`` -- Only displays the HTML element inline for screen sizes less than or equal to the
      upper limit for ``small`` screen sizes.
    - ``'green-medium-up'`` -- Set ``color`` to green for screen sizes greater than or equal to the lower limit
      for ``medium`` size screens.

    **Custom Usage: Set a specific pixel limit.**
    - ``'display-480px-down'`` -- Only displays the HTML element inline for screen sizes less than or equal to 480px.
    - ``'bold-624-up'`` -- Set the ``font-weight`` to ``bold`` for screen sizes greater than or equal to 624px.
      Note: If unit conversion is enabled i.e. ``px_to_em`` is ``True``, then 624px would be converted to 39em.

    :type css_class: str
    :type px_to_em: bool

    :param css_class: Potentially encoded css class that may or may not be parsable.
    :param px_to_em: A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion.
        False disables unit conversions meaning any pixel value remains unchanged.
    :return: None

    **Examples:**

    >>>

    """

    def __init__(self, css_class='', px_to_em=True):
        # Default Screen Width Settings
        # Tuple Format (Lower Limit, Upper Limit) in pixels.
        # Note: If unit conversion is enabled i.e. ``px_to_em`` is ``True``, then all values are converted to 'em'.
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

        self.direction_set = {
            '-only', '-down', '-up'
        }



    # TODO: Implement media query handling using:


    # TODO: Handle font-family names with dashes in them same thing for "voice-family"
    # TODO: Consider using '--' to represent '-' dash could be an escape character
    # e.g. font: 15px sans-serif OR font: sans-serif 15px OR font-family: sans-serif
    # ERROR font-15px-sans-serif --> font: 15px sans serif
    # Might require a font name dictionary.
    # What about commas?
    # Could just use font-family name explicity e.g. sans-serif, arial, source-sans-pro
    # x--large --> x*d*large --> x-large
    # OR
    # Setting everything to lowercase.
    # Find all dashed keywords x-large san-serif etc.
    # Replace with uppercase X-LARGE SAN-SERIF
    # Remove all '-' dashes except the ones between uppercase letters.

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
