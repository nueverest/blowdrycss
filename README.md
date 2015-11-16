# blowdrycss
Tool used to quickly auto-generate DRY CSS from encoded classes found in *.html, *.aspx, *.ascx, or *.master files. 
Add your own file extensions under `filehandler.py: FileFinder.file_types`.

### Example Usage in HTML Tags:
```html
<div class="text-align-center margin-top-30">
    <p class="font-size-25">The font-size is 25px. <span class="green">Green Text</span></p>
</div>
```

blowdrycss decodes the class names `text-align-center`, `margin-top-30`, `font-size-25`, and `green`; and generates
the following CSS in `blowdry.css`:
```css
.text-align-center { text-align: center }
.margin-top-30 { margin-top: 30px }
.font-size-25 { font-size: 25px }
.green { color: green }
```

# Requirements
Python 3.4+ (required)

cssutils 1.0.1+ (required)

unittest (run unit tests)

coverage 4.0.2+ (check test coverage)

# How to Run the '/ExampleSite' demo
:one: Download the project

:two: Navigate to `../blowdrycss/python` directory

:three: Run `pip install -r requirements.txt`

:four: Run `python blowdry` 

:five: Navigate to `../blowdrycss/ExampleSite/css` there should be a `blowdry.css` and `blowdry.min.css` file there.

Feel free to delete these two files and re-run `python blowdry` to confirm that these two files are auto-generated.
These two files are not intended to be edited by humans.  Any manual changes made to these two files are overwritten
when `python blowdry` is run.

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

### Advantages of blowdrycss
:one: Rapid Development: Less time spent writing CSS, and cleaning up unused properties.

:two: DRY (Don't Repeat Yourself): Reduces the size of CSS file by only defining properties once.

:three: Greater confidence that your CSS is not filled with unused or over-replicated class definitions.

:four: Built for the real world in which deadlines and division of labor is not always taken into account.

:five: Integrated minification.

:six: Parameter customization.

:seven: PEP8 Compliant

:eight: Full UnitTest Coverage

:nine: MIT License

### What it is not
This tool is not designed to replace the need to hand-craft complex CSS.  Multi-rule classes, Background images, 
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
Encoded Class | Property Name or Alias | Property Value | CSS Rule Output
------------- | ---------------------- | -------------- | ---------------
font-size-25 | font-size- | 25 | .font-size-25 { font-size: 25px }
green | color- | green | .green { color: green }
p-70-10 | p- | 70px 10px | .p-70-10 { padding: 70px 10px }

### Encoded Class Format Rules
##### Dashes separate words in multi-word property names/aliases.
`font-weight`

##### Property names may be encoded as an alias.
Consider this dictionary key, value pair found in `datalibrary.py` dictionary 
`DataLibrary.self.custom_property_alias_dict`.

`'font-weight': {'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'},`

It maps the alias set `{'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'}` to the property name
`font-weight`. Meaning that any of the values in the set can be substituted for `font-weight`. 

The full property name can also be used in the encoded class i.e. `font-weight-`.

##### Dashes separate CSS property name/alias from property value
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
property-name-value | .property-name-value { property-name: value }
alias-value | .alias-value { property-name: value }
font-weight-700 | .font-weight-700 { font-weight: 700 }
fw-700 | .fw-700 { font-weight: 700 }

##### Dashes separate multiple values for properties that take multiple values.
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
alias-value-value-value-value | .alias-value-value-value-value { property-name: value value value value }
padding-10-20-10-10 | .padding-10-20-10-10 { padding: 10px 20px 10px 10px }
p-10-20-10-10 | .p-10-20-10-10 { padding: 10px 20px 10px 10px }

##### Dashes separate `!important` priority indicator `'-i'` (append to the end of the string)
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
alias-value-i | .alias-value-i { property-name: value !important }
font-weight-bold-i | .font-weight-bold-i { font-weight: bold !important }

##### Shorthand can be used in cases where the alias is unambiguously the value.
Applicable properties include: `color`, `font-weight`, `font-style`, `text-decoration`, and `text-transform`.

Encoded Class Format | CSS Rule Output
--------------------- | ---------------
alias | .alias { property-name: alias }
purple | .purple { color: purple }
bold | .bold { font-weight: bold }
lighter | .lighter { font-weight: lighter }
underline | .underline { text-decoration: underline }
italic | .italic { font-style: italic }
lowercase | .lowercase { text-transform: lowercase }

##### Color Declarations
Color Format | Encoded Class Format | CSS Rule Output
------------ | --------------------- | ---------------
keyword | color-silver | .color-silver { color: silver }
 rgb | color-rgb-0-255-0 | .color-rgb-0-255-0 { color: rgb(0, 255, 0) }
rgba | color-rgba-255-0-0-0_5 | .color-rgba-255-0-0-0_5 { color: rgba(255, 0, 0, 0.5) }
hex6 | color-h0ff23f (prepend 'h') | .color-h0ff23f { color: &#35;0ff23f }
hex3 | color-h03f    (prepend 'h') | .color-h03f { color: &#35;03f }
 hsl | color-hsl-120-60p-70p | .color-hsl-120-60p-70p { color: hsl(120, 60%, 70%) }
hsla | color-hsla-120-60p-70p-0_3 | .color-hsla-120-60p-70p-0_3 { color: hsl(120, 60%, 70%, 0.3) }

##### Negative Values 
'n' :point_right: '-'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'n48' | '-48'
'n5cm n6cm' | '-5cm -6cm'
'n9in' | '-9in' 
###### Note that the 'n' at the end of `-9in` is not affected.

##### Use underscores to indicate Decimal point.
'1_25' :point_right: '1.25'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'1_32rem' | '1.32rem'

###### Special Note: Underscores can 'only' be used as decimal points.  
Other usage of underscores will invalidate the class. e.g. 'padding_1', '_padding-1', or 'padding-1_' 
are considered invalid and will not be decoded. Classes may still be defined with these names, but CSS would not 
be generated by this tool.

##### Using Percentages 'p' becomes '%'
'p' :point_right: '%'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'1p-10p-3p-1p' | '1% 10% 3% 1%'
'32p' | '32%'

##### Default Units:
If units are not provided in the class name, then default units were applicable. The default units
are defined in `DataLibrary.default_property_units_dict` inside `datalibrary.py`.  This makes it possible to
easily change the default units for a particular property name.

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
padding-50| padding: 50px
elevation-20 | elevation: 20deg

##### Explicitly Encoding Units in Class Name

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
padding-50cm | padding: 50cm
width-120vmin | width: 120vmin

### Good to know
##### Find Non-matching classes
If the encoded class name contains a typo or invalid value 
e.g. `ppadding-5`, `margin-A`, `font-color-h000rem`, or `squirrel-gray` 
it will be placed in `removed_class_set`.  The variable `removed_class_set` is found in `ClassPropertyParser()` inside 
of `classpropertyparser.py`.

##### Customize Aliases:
:one: Open `python/datalibrary.py`

:two: In the `DataLibrary` class edit `self.custom_property_alias_dict`

##### Change the CSS File Name and Location:
TODO: Document how easy it is to edit blowdry.py

### Upcoming Features:
##### Make DRYer:
TODO: Implement this essential feature.
TODO: Document
Currently two classes are being created with the same properties.  The preferred solution would be to assign
both classes to the same property.

###### Scenario 1:
bold | .bold { font-weight: bold }
font-weight-bold | .font-weight-bold { font-weight: bold }
###### DRY solution 1
.bold, font-weight-bold { font-weight: bold }   (preferred)

###### Scenario 2:
padding-10 | .padding-10 { padding: 10px }
padding-10px | .padding-10px { padding: 10px }
###### DRY solution 2
.padding-10, .padding-10px { padding: 10px }    (preferred)

##### Drop requirement for hexadecimal color values to be prefixed with a property name.

Color Format | Encoded Class Format | CSS Rule Output
------------ | --------------------- | ---------------
hex6 | h0ff23f | .h0ff23f { color: C&#35;0ff23f }
hex3 | hfd4 | .hfd4 { color: C&#35;fd4 }

##### Trigger automatic CSS generation on file change:
In the event that a file with a designated extension is saved.  Preferably without tons of dependencies or polling.
TODO: Implement this essential feature.
TODO: Document

##### Automatic px :point_right: rem Unit Conversion:
TODO: Implement this really cool feature.
TODO: Document

##### Create Seamless Media Queries for responsive layouts:
TODO: Implement this really cool feature.
TODO: Document

##### Build Responsive Fonts with -r:
TODO: Implement this really cool feature.
TODO: Document
font-size-25-r

##### Sphinx Integration
TODO: Integrate Sphinx
TODO: Put the docs on readthedocs 

##### Implement using Javascript (consider what this would require)
TODO: Implement this really cool feature.
TODO: Document

### Unsupported Features:
##### Shorthand properties
Use shorthand properties at your own risk. Currently no support is guaranteed for shorthand properties.

##### No encoding is defined for '/', comma, dash, double quote, '@'.
font: 12px/14px sans-serif | '/' and '-' encoding not available
font: 16rem "New Century Schoolbook" | double quote encoding not available
font-family: Palatino, serif, arial | comma encoding not available

##### Properties Values that contain 'url()' are not supported as they are too bulky and verbose. These sorts of
declarations belong in your custom CSS class definitions.
background-image: url("/home/images/sample/image.png")

##### Some Encoded Property Values containing '-' will become invalid.
font-family-sans-serif| font-family: sans serif (invalid)
font-size-x-large| font-size: x large      (invalid)

##### That said "some cases will work" (note that in these examples the units of 'px' are explicitly declared:
font-30px-arial | font: 30px arial                (valid)
font-italic-bold-12px-serif | font: italic bold 12px serif    (valid)

### Valuable Reference:
W3C Full CSS property table: http://www.w3.org/TR/CSS21/propidx.html

### How to Contribute
Raise Issues
Write Code

Vote for features with a donation. Your contribution directs focus on the most desired features first. Keep in mind
that all of the time estimates include documentation and unit testing. As features are implemented and donations 
received the table is manually updated.

Feature | Goal | Time | Received | Complete | Donate Here
------- | ---- | ------------- | --------------------- | -------------- | -----------
Make DRYer. | $300 | 4-6 hr | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=EY63EWAXXVKJ2)
Enable hexadecimal color aliases. | $300 | 4-6 hr | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SGQX89U2N7XAN)
Auto-generate CSS on save. | $200 | 3-4 hr | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=HFU4TJXGB75CW)
Automatic px to rem Unit Conversion | $150 | 2-3 hr | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V3DQMK4Q3SJTC) 
Media Queries for responsive style | $1,248 | 2-4 days | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=E4LEBP5EYSE9N)
Responsive Scaling Fonts '-r' | $200 | 3-4 hr | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BJMHSE7NDSKVU)
Sphinx Integration | 1-2 wks | $2,000 | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=MWGFYZZ4DXD2N)
Port to Javascript | $10,000 | 1-2 mo | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9NEXW8MRMUXAU)
Suggest a Feature | ----- | ----- | $0 | 0% | [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ENEWAE88R4LGG)

