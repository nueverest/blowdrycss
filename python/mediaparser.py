__author__ = 'chad nelson'
__project__ = 'blow dry css'


class MediaParser(object):
    def __init__(self):
        pass

    # TODO: Implement media query handling using:
    # allow user to define a dict
    # 'xxsmall', 'xxs': (0, 120),
    # 'xsmall', 'xs': (0, 240),
    # 'small', 's', 'sm': (0, 480), etc...
    #
    # hide-for-, show-for-
    # -small-only, -small-down, -small-up, hide-for-480px-down, show-for-480px-up, hide-for-480-down, show-for-480-down

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
