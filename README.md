# BlowDryCSS
Tool used to auto-generate DRY CSS from encoded classes for in *.html, *.aspx, *.ascx, *.master, or add your own
file extension under FileFinder.file_types.

TODO: Provide simple instructions for how to get up and running quickly.

### Motivation
This tool was created after seeing how many companies manage their CSS files. The following are a couple of
scenarios.

##### Scenario 1 - Inside a CSS file you find the following:
```css
.header-1 { font-weight: bold; font-size: 12px; font-color: red; }
.header-2 { font-weight: bold; font-size: 16px; font-color: blue; }
.header-3 { font-weight: bold; font-size: 12px; font-color: green; }
```
    
The property `font-weight: bold;` appears three times, and `font-size: 12px;` appears twice. This is not 
DRY (Don't Repeat Yourself).

Six months later the person who wrote this CSS is then asked to remove header-2 and header-3 from the homepage.
More often than not the front-end developer will remove the CSS class from the HTML file, but not from the CSS file.

###### Some reasons for this include:
* Forgetting to delete the rule from the CSS file.
* Fear that the class is used somewhere else and that it might break the site.
* Being too busy to search all of the files in their project for other potential use cases.

The result is that multiple kilobytes worth of unused, dead CSS data remain.

##### Scenario 2 - CSS Pre-compiler:
CSS pre-compilation with SASS/SCSS or LESS is awesome, and makes writing lots of CSS rules easy. For instance, you can
now auto-generate hundreds of header rules like the ones above if care is not taken. The power of the pre-compiler
represents a double edged sword.

###### SCSS Mixin example from a recent project:

```css
@mixin text($font-color, $font-size, $font-family:"Open Sans", $line-height:inherit) {
    color: $font-color;
    font-size: $font-size;
    font-family: $font-family, $default-font-family;
    line-height: $line-height;
}
```
    
This mixin is called using `@include` as follows:
`@include text($color-blue, rem-calc(14px), $default-font-family);`

It turns out that `@include text(...)` is called 627 times in our SCSS.  Most of these `@include` statements include
at least one matching input parameter resulting in thousands of duplicate CSS properties.

Auto-generating `font-size: 1rem;` 500 times is now super easy with a pre-compiler. 
Some might say, 
> Well we minified it to save space.
 
Yes but, 
> Why did you write the same property 500 times into your main CSS file?

###### CSS File size does matter. Large style files result in the following:
* Longer download times increase bounce rates.
* Data pollution on the Internet. 
* Increase the likelihood of style bugs.
* Increase the amount of time required to implement new changes and deprecate features.

### Advantages of BlowDryCSS
:one: Rapid Development: Less time spent writing CSS, and cleaning up unused properties.

:two: DRY (Don't Repeat Yourself): Reduces the size of CSS file by only defining properties once.

:three: Greater confidence that your CSS is not filled with unused or over-replicated class definitions.

:four: Built for the real world in which deadlines and division of labor is not always taken into account.

:five: Integrated minification.

:six: PEP8 Compliant

:seven: Full UnitTest Coverage

### What it is not
This tool is not designed to replace the need to manually develop complex CSS.  Multi-rule classes, Background images, 
url() values, and shorthand properties are not fully supported.

The following is an example of something this tool in not intended to generate, and something that still needs to
be written by hand.
    
```css
.home-banner {
    min-height: 191px;
    background: url("https://somewhere.net/images/banner/home-mainbanner-bg.jpg") no-repeat;
    background-size: 100% 100%;
    color: white;
    font-size: 3.5625rem;
    font-family: "Gentium Book Basic","Open Sans","Source Sans Pro",Arial;
    line-height: 3.6875rem;
    text-align: center;
    background-size: cover;
    background-repeat: no-repeat;
    min-height: 7rem;
    text-shadow: -2px 2px 4px rgba(0,0,0,0.5);
    font-family: "Open Sans","Source Sans Pro",Arial;
}
```
    
### Dissecting Encoded CSS Classes
encoded class == font-size-25
property_name/alias = 'font-size'
property_value = '25'

### Example Usage in HTML Tag:
`<p class="font-size-25">The font-size is 25px.</p>`

`font-size-25` gets automatically decoded by this script becoming `.font-size-25 { font-size: 25px }` in the generated
 CSS file.

### Encoded Classes Format Rules
##### Dashes separate words in multi-word property names/aliases.
`font-weight`

##### Property names may be encoded as an alias.
Consider this dictionary entry found in `datalibrary.py`
`'font-weight': {'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'},`

It maps the alias set `{'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'}` to the propert name
`font-weight`. Meaning that any of the values in the set can be substituted for `font-weight`

##### Dashes separate CSS property name/alias from property value
Class Encoding Format | CSS Rule Output
--------------------- | ---------------
font-weight-700 | .font-weight-700 { font-weight: 700 }
fw-700 | .fw-700 { font-weight: 700 }

##### Dashes separate multiple values for properties that take multiple values.
alias-value-value-value-value
padding-10-20-10-10                     --> padding: 10px 20px 10px 10px
p-10-20-10-10                           --> padding: 10px 20px 10px 10px

##### Dashes separate `!important` priority indicator `'-i'` (append to the end of the string)
alias-value-i
font-weight-bold-i                      --> font-weight: bold !important

##### Shorthand can be used in cases where the alias is the unambiguously the value.
alias == value
font-weight-bold                        --> font-weight: bold
bold                                    --> font-weight: bold

##### Color Declarations:
 rgb: font-color-rgb-0-255-0            --> font-color: rgb(0, 255, 0)
rgba: font-color-rgba-255-0-0-0_5       --> font-color: rgba(255, 0, 0, 0.5)
hex6: font-color-h0ff23f (prepend 'h')  --> font-color: #0ff23f
hex3: font-color-h03f    (prepend 'h')  --> font-color: #03f
 hsl: font-color-hsl-120-60p-70p        --> font-color: hsl(120, 60%, 70%)
hsla: font-color-hsla-120-60p-70p-0_3   --> font-color: hsl(120, 60%, 70%, 0.3)

##### Negative Values ('n' --> '-')
'n5cm n6cm'                             --> '-5cm -6cm'
'n9in'                                  --> '-9in' (note that the 'n' at the end is not touched)

Use underscores to indicate Decimal point.
'_' becomes '.'
'1_32rem' --> '1.32rem'

Note: Underscores can only be used in this way.  Other usage of underscores will invalidate the class.
e.g. 'padding_1', '_padding-1', or 'padding-1_' are considered invalid and will not be decoded.
You could still define classes with these names, but CSS would not be automatically generated. You would need
to create CSS manually for unrecognized classes.

Using Percentages 'p' becomes '%'
alias-valuep
'1p-10p-3p-1p'  --> '1% 10% 3% 1%'
'32p'           --> '32%'

Default Units:
If units are not provided in the class name the script will assign default units were possible.
padding-50      --> padding: 50px
elevation-20    --> elevation: 20deg

Encoding Units in Class Name
padding-50cm    --> padding: 50cm
width-120vmin   --> width: 120vmin

Customize Aliases:
TODO: Document how easy it is to change alter dictionaries.

Change the CSS File Name and Location:
TODO: Document how easy it is to edit blowdry.py

### Upcoming Features:
Make DRYer:
TODO: Implement this essential feature.
TODO: Document
Currently two classes are being created with the same properties.  The preferred solution would be two assign
both classes to the same property.

Scenario 1:
bold                --> .bold { font-weight: bold }
font-weight-bold    --> .font-weight-bold { font-weight: bold }
DRY solution 1      --> .bold, font-weight-bold { font-weight: bold }   (preferred)

Scenario 2:
padding-10          --> .padding-10 { padding: 10px }
padding-10px        --> .padding-10px { padding: 10px }
DRY solution 2      --> .padding-10, .padding-10px { padding: 10px }    (preferred)

Trigger automatic CSS generation on file change:
In the event that a file with a designated extension is saved.
TODO: Implement this essential feature.
TODO: Document

Automatic px --> rem Unit Conversion:
TODO: Implement this really cool feature.
TODO: Document

Create Seamless Media Queries for responsive layouts:
TODO: Implement this really cool feature.
TODO: Document

Build Responsive Fonts with -r:
TODO: Implement this really cool feature.
TODO: Document
font-size-25-r

Allow Class Encodings to match Zen CSS / Emmet Cheatsheet abbreviations
TODO: Implement this really cool feature.
TODO: Document

### Unsupported Features:
##### Shorthand properties
Use shorthand properties at your own risk. Currently no support is guaranteed for shorthand properties.

##### No encoding is defined for '/', comma, dash, double quote, '@'.
font: 12px/14px sans-serif              --> '/' and '-' encoding not available
font: 16rem "New Century Schoolbook"    --> double quote encoding not available
font-family: Palatino, serif, arial     --> comma encoding not available

##### Properties Values that contain 'url()' are not supported as they are too bulky and verbose. These sorts of
declarations belong in your custom CSS class definitions.
background-image: url("/home/images/sample/image.png")

##### Some Encoded Property Values containing '-' will become invalid.
font-family-sans-serif                  --> font-family: sans serif (invalid)
font-size-x-large                       --> font-size: x large      (invalid)

##### That said "some cases will work" (note that in these examples the units of 'px' are explicitly declared:
font-30px-arial                         --> font: 30px arial                (valid)
font-italic-bold-12px-serif             --> font: italic bold 12px serif    (valid)

### Valuable Reference:
W3C Full CSS property table: http://www.w3.org/TR/CSS21/propidx.html
