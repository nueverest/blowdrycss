# blowdrycss
Tool used to quickly auto-generate DRY CSS files from encoded classes found in *.html, *.aspx, *.ascx, or 
*.master files.
<br>Other file extensions can be add under `filehandler.py: FileFinder.file_types`.

#### Why the name blowdrycss?
Inspiration for the name came from the blow dryer. A blow dryer rapidly drys and styles hair. :ok_woman: 

Similarly, `blowdrycss` is used to rapidly style HTML and generate DRY CSS files using encoded class names.

##### Decomposition
> **Blow** means to expel a current of air causing it to be in a state of motion.<br>
  **DRY** stands for Don't Repeat Yourself.<br>
  **CSS** stands for Cascading Style Sheets.

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
[Python 3.4+](https://www.python.org/downloads/) (required)
<br>[cssutils 1.0.1+](https://bitbucket.org/cthedot/cssutils) (required)
<br>[watchdog 0.8.2+](https://pypi.python.org/pypi/watchdog/0.8.3) (desired)
<br>unittest (run unit tests)
<br>coverage 4.0.2+ (check test coverage)

# Pre-Requisite Knowledge
* Basic HTML, CSS, and Python skills.

# Basic Tutorial
## How to Run the '/examplesite' demo
### Part 1 - Start the web browser to view the unstyled examplesite.
* Download the project
* Navigate to `../blowdrycss/examplesite`
* Run `python -m http.server 8080` (Python 3.x) or `python -m SimpleHTTPServer 8080` (Python 2.x)
* Open a web browser and go to [localhost:8080](http://localhost:8080)
* The page should contain lots of un-styled text and images.

### Part 2 - Auto-generate CSS
* Navigate to `../blowdrycss/python`
* Run `pip install -r requirements.txt` If pip is not install [go here](https://pip.pypa.io/en/latest/installing/).
* Run `python blowdry.py` 
* Navigate to `../blowdrycss/examplesite/css` and verify that `blowdry.css` and `blowdry.min.css` now exist.
* Open a web browser and go to [localhost:8080](http://localhost:8080). 
* The page should now be styled better.

### Part 3 - Apply new styles in `index.html`
##### Lets actually change something.
* Navigate to `../blowdrycss/examplesite`
* Open `index.html`
* Find the line `<h1 class="c-blue text-align-center">Blow Dry CSS</h1>`
* From the class attribute delete `c-blue` and replace it with the word `green`
* Add the class `font-size-148`
* The line should now look like this `<h1 class="green font-size-148 text-align-center">Blow Dry CSS</h1>`
* Now refresh the web page running on [localhost:8080](http://localhost:8080).
* What happened? Nothing happened because you need to run `blowdry.py`
* Navigate to `../blowdrycss/python`
* Run `python blowdry.py` 
* Now refresh the web page running on [localhost:8080](http://localhost:8080).
* The title at the top of the page should be large and green.
* Let's make some more changes.
* Center the image below the title with the class `t-align-center` in the `<div>` containing the image.
* Find the `+` images and add the class `padding-bottom-4p` directly to the `img` class attribute.
* Run `python blowdry.py` 
* Now refresh the web page running on [localhost:8080](http://localhost:8080).
* Feel free to continue experimenting with different property names and values.  More information about how to form
write well-form encoded class names is found further down this page.

### Part 4 - Setup Watchdog
* At this point having to run `python blowdry.py` could be getting annoying.
* What if it were possible to detect that `index.html` was saved and run `python blowdry.py` automatically?
    * This is possible with [`watchdog`](https://pypi.python.org/pypi/watchdog/0.8.3).
* To setup watchdog run `pip install watchdog`
* Navigate to `/examplesite` at the command line.
* From the command line run:
`watchmedo shell-command --patterns="*.html;" --ignore-directories --recursive --command="python ../python/blowdry.py"`
* Now add the class `margin-150` to one of the `<div>` tags, and save `index.html`
* Refresh [localhost:8080](http://localhost:8080) in the browser, and the change should appear without manually 
re-running `blowdry.py`.

###### What if refreshing the browser doesn't work?
* Ensure `watchdog` is running.
* Check the shell or command prompt where `watchog` is running to see if there are any error messages.
* Double check that the command is running in the correct directory, and that the python command will run from the
directory without `watchdog`.

##### Watchdog Parameter Modification
`--patterns` can be set to any file type that should trigger `blowdry.py`.
For example: `--patterns="*.html;*.aspx;*.js"`

`--recursive` causes the `watchdog` to monitor all of the files matching `--patterns` in all subdirectories 
of the current folder.

`--ignore-directories` ignores all directory related events, and only focuses on file changes.

`--command` contains the path to `blowdry.py`. Make sure that this is the correct directory otherwise it will not run.

### Part 5 - Experiment with these classes
* Apply these to an image: `border-10px-solid-black` `p-20-30-20-30` `w-50`
* Apply this to a div: `display-none`
* Apply this to text: `uppercase`

##### Notes about the auto-generated `*.css` files
The CSS files `blowdry.css` and `blowdry.min.css` are not intended to be edited by humans.  
Any manual changes made to these two files are overwritten when `python blowdry.py` is run.

# Motivation
This tool was created after seeing how many companies manage their CSS files. The following are a couple of
scenarios.

#### Scenario 1 - Inside a CSS file you find the following:
```css
.header-1 { font-weight: bold; font-size: 12px; font-color: red; }
.header-2 { font-weight: bold; font-size: 16px; font-color: blue; }
.header-3 { font-weight: bold; font-size: 12px; font-color: green; }
```
    
The property `font-weight: bold;` appears three times, and `font-size: 12px;` appears twice. This is not 
DRY (Don't Repeat Yourself).

Six months later the person who wrote this CSS is then asked to remove header-2 and header-3 from the homepage.
More often than not the front-end developer will remove the CSS class from the HTML file, but not from the CSS file.

##### Some reasons for this include:
* Forgetting to delete the rule from the CSS file.
* Fear that the class is used somewhere else and that it might break the site.
* Being too busy to search all of the files in their project for other potential use cases.

The result is that multiple kilobytes worth of unused, dead CSS data remain.

#### Scenario 2 - CSS Pre-compiler:
CSS pre-compilation with SASS/SCSS or LESS is awesome, and makes writing lots of CSS rules easy. For instance, you can
now auto-generate hundreds of header rules like the ones above if care is not taken. The power of the pre-compiler
represents a double edged sword.

##### SCSS Mixin example from a recent project:

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
 
###### Yes but, 
> Why did you write the same property 500 times into your main CSS file? :hear_no_evil: :see_no_evil: :speak_no_evil:

##### CSS File size does matter. Large style files result in the following:
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
    background: url("https://somewhere.net/images/banner/home-mainbanner-bg.jpg") no-repeat;
    font-family: "Open Sans","Source Sans Pro",Arial;
    background-repeat: no-repeat;
    background-size: cover;    
    min-height: 7rem;
    font-weight: bold;
    font-size: 3.5625rem;
    color: white;    
    line-height: 3.6875rem;
    text-align: center;
    text-shadow: -2px 2px 4px rgba(0,0,0,0.5);
}
```

#### DRY-ness must be balanced against other factors.  
The first three properties are not currently supported by `blowdrycss`. Eight out of the eleven style lines or 72% 
of the lines could be written by hand as encoded classes. However, it would result in the following really long class 
attribute:  

```html
<div class="background-size-cover min-h-7rem bold font-size-3_5625rem white line-height-3_6875rem talign-center 
            t-shadow-n2px-2px-4px-rgba-0-0-0-0_5">
    <!-- div contents -->
</div>
```

This is a case were the DRY principle is subsumed by the value of readability, brevity, and encapsulation. Also, just
because this tool can decode the class `t-shadow-n2px-2px-4px-rgba-0-0-0-0_5` that doesn't mean it is intended to
be used in this manner.

#### My CSS is DRY, but my HTML is not.
Copying and pasting something like `p-10 h-50 w-50 talign-center orange font-size-16` twenty times in an HTML file 
is not that DRY either. If this is happening, then it might be valuable to pause and hand-craft a CSS class for 
this repeating class pattern.  

# Encoded Class Formatting and Rules

### Dissecting Encoded CSS Classes
Encoded Class | Property Name or Alias | Property Value | CSS Rule Output
------------- | ---------------------- | -------------- | ---------------
font-size-25 | font-size- | 25 | .font-size-25 { font-size: 25px }
green | color- | green | .green { color: green }
p-70-10 | p- | 70px 10px | .p-70-10 { padding: 70px 10px }

### Dashes separate words in multi-word property names and aliases.
###### A Property Names is a valid CSS property name in accordance with the [W3C Full CSS property table](http://www.w3.org/TR/CSS21/propidx.html)

`font-weight, border-bottom-color, border-bottom-style, border-bottom-width, border-collapse`

###### Aliases for property names.
`f-weight-, bg-c-, bg-color-, t-align-`

### Dashes are placed at the end of aliases to indicate that it's an alias and not a css property name.

### Property names may be encoded as an alias.
Consider this dictionary key, value pair found in `datalibrary.py` dictionary 
`DataLibrary.self.custom_property_alias_dict`.

`'font-weight': {'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'},`

It maps the alias set `{'fweight-', 'lighter', 'fw-', 'bolder', 'f-weight-', 'font-w-', 'bold'}` to the property name
`font-weight`. Meaning that any of the values in the set can be substituted for `font-weight`. 

The full property name can also be used in the encoded class i.e. `font-weight-`.

### Dashes separate CSS property name/alias from property value
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
property-name-value | .property-name-value { property-name: value }
alias-value | .alias-value { property-name: value }
font-weight-700 | .font-weight-700 { font-weight: 700 }
fw-700 | .fw-700 { font-weight: 700 }

### Dashes separate multiple values for properties that take multiple values.
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
alias-value-value-value-value | .alias-value-value-value-value { property-name: value value value value }
padding-10-20-10-10 | .padding-10-20-10-10 { padding: 10px 20px 10px 10px }
p-10-20-10-10 | .p-10-20-10-10 { padding: 10px 20px 10px 10px }

### Dashes separate `!important` priority indicator `'-i'` (append to the end of the string)
Encoded Class Format | CSS Rule Output
--------------------- | ---------------
alias-value-i | .alias-value-i { property-name: value !important }
font-weight-bold-i | .font-weight-bold-i { font-weight: bold !important }

### Shorthand can be used in cases where the alias is unambiguously the value.
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

### Color Declarations
Color Format | Encoded Class Format | CSS Rule Output
------------ | --------------------- | ---------------
keyword | color-silver | .color-silver { color: silver }
 rgb | color-rgb-0-255-0 | .color-rgb-0-255-0 { color: rgb(0, 255, 0) }
rgba | color-rgba-255-0-0-0_5 | .color-rgba-255-0-0-0_5 { color: rgba(255, 0, 0, 0.5) }
hex6 | color-h0ff23f (prepend 'h') | .color-h0ff23f { color: &#35;0ff23f }
hex3 | color-h03f    (prepend 'h') | .color-h03f { color: &#35;03f }
 hsl | color-hsl-120-60p-70p | .color-hsl-120-60p-70p { color: hsl(120, 60%, 70%) }
hsla | color-hsla-120-60p-70p-0_3 | .color-hsla-120-60p-70p-0_3 { color: hsl(120, 60%, 70%, 0.3) }

### Negative Values 
'n' :point_right: '-'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'n48' | '-48'
'n5cm n6cm' | '-5cm -6cm'
'n9in' | '-9in' 
###### Note that the 'n' at the end of `-9in` is not affected.

### Use underscores to indicate Decimal point.
'1_25' :point_right: '1.25'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'1_32rem' | '1.32rem'

###### Special Note: Underscores can 'only' be used as decimal points.  
Other usage of underscores will invalidate the class. e.g. 'padding_1', '_padding-1', or 'padding-1_' 
are considered invalid and will not be decoded. Classes may still be defined with these names, but CSS would not 
be generated by this tool.

### Using Percentages 'p' becomes '%'
'p' :point_right: '%'

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
'1p-10p-3p-1p' | '1% 10% 3% 1%'
'32p' | '32%'

### Default Units:
If units are not provided in the class name, then default units were applicable. The default units
are defined in `DataLibrary.default_property_units_dict` inside `datalibrary.py`.  This makes it possible to
easily change the default units for a particular property name.

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
padding-50| padding: 50px
elevation-20 | elevation: 20deg

### Explicitly Encoding Units in Class Name

Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
padding-50cm | padding: 50cm
width-120vmin | width: 120vmin

# Good to know
### Find Non-matching classes
If the encoded class name contains a typo or invalid value 
e.g. `ppadding-5`, `margin-A`, `font-color-h000rem`, or `squirrel-gray` 
it will be placed in `removed_class_set`.  The variable `removed_class_set` is found in `ClassPropertyParser()` inside 
of `classpropertyparser.py`.

### Customize Aliases:
:one: Open `python/datalibrary.py`

:two: In the `DataLibrary` class edit `self.custom_property_alias_dict`

### Change the CSS File Name and Location:
TODO: Document how easy it is to edit blowdry.py

# Upcoming Features:
### Make DRYer:
TODO: Implement this essential feature.
<br>TODO: Document
Currently two classes are being created with the same properties.  The preferred solution would be to assign
both classes to the same property.

###### Scenario 1:
Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
bold | .bold { font-weight: bold }
font-weight-bold | .font-weight-bold { font-weight: bold }

Duplicates the string `{ font-weight: bold }`.

###### DRY solution 1
```css
.bold, font-weight-bold { font-weight: bold }
```   

###### Scenario 2:
Value Encoding Format | CSS Property Value Output
--------------------- | -------------------------
padding-10 | .padding-10 { padding: 10px }
padding-10px | .padding-10px { padding: 10px }

Duplicates the string `{ padding: 10px }`

###### DRY solution 2
```css
.padding-10, .padding-10px { padding: 10px }
```

##### Drop requirement for hexadecimal color values to be prefixed with a property name.

###### Allow

Color Format | Encoded Class Format | CSS Rule Output
------------ | --------------------- | ---------------
hex6 | h0ff23f | .h0ff23f { color: C&#35;0ff23f }
hex3 | hfd4 | .hfd4 { color: C&#35;fd4 }

##### Automatic px :point_right: rem Unit Conversion:
TODO: Implement this really cool feature.
<br>TODO: Document

##### Create Seamless Media Queries for responsive layouts:
TODO: Implement this really cool feature.
<br>TODO: Document

##### Build responsive scaling fonts using -r:
TODO: Implement this really cool feature.
<br>TODO: Document

###### Encoded Class 
font-size-25-r

###### Resulting CSS media query.
TODO: Add CSS here.
```css
.font-size-25-r {
    font-size: 25px;
}
```

##### Sphinx Integration
TODO: Integrate Sphinx
<br>TODO: Put the docs on readthedocs 

##### Implement using Javascript (consider what this would require)
TODO: Implement this really cool feature.
<br>TODO: Document

##### Support basic Tween Capability from GreenSock
 TODO: Implement (out of scope for the near future)
 <br>TODO: Document dependencies and basic usage.

##### DRY CSS File Analyzer (possibly belongs in a separate project)
TODO: Return statistics on how many times a given property value appears in a CSS File.
<br>TODO: Document

# Unsupported Features:
##### Shorthand properties
Use shorthand properties at your own risk. Currently no support is guaranteed for shorthand properties.

##### No encoding is defined for '/', comma, dash, double quote, '@'.

CSS Property Value | Encodings Not Implemented  
------------------ | -------------------------
font: 12px/14px sans-serif | '/' and '-'
font: 16rem "New Century Schoolbook" | double quote
font-family: Palatino, serif, arial | comma

##### Properties Values that contain 'url()' are not supported as they are too bulky and verbose. These sorts of
`url()` declarations belong in your custom CSS class definitions. 

CSS Property Value | Encodings Not Implemented  
------------------ | ------------------------- 
background-image: url("/home/images/sample/image.png") | '/', '(', and double quote

##### Some Encoded Property Values containing '-' will become invalid.
That said "some cases will work". Note that in the valid examples the units of 'px' are explicitly declared.

Value Encoding Format | CSS Property Value Output | Validity
--------------------- | ------------------------- | :------:
font-family-sans-serif | font-family: sans serif | invalid missing dash
font-size-x-large | font-size: x large | invalid missing dash
font-30px-arial | font: 30px arial | valid
font-italic-bold-12px-serif | font: italic bold 12px serif | valid

### Valuable Reference
[W3C Full CSS property table](http://www.w3.org/TR/CSS21/propidx.html)
[cssutils](https://bitbucket.org/cthedot/cssutils)

### License
The MIT License (MIT)

### How to Contribute
* Report Issues
* Write Code
* [Flattr this Project](https://flattr.com/submit/auto?user_id=nueverest&url=https%3A%2F%2Fgithub.com%2Fnueverest%2Fblowdrycss) 
<br>&nbsp;&nbsp;&nbsp;<a href="https://flattr.com/submit/auto?user_id=nueverest&url=https%3A%2F%2Fgithub.com%2Fnueverest%2Fblowdrycss" target="_blank"><img src="http://button.flattr.com/flattr-badge-large.png" style="text-align:bottom;" alt="Flattr this" title="Flattr this" border="0"></a>


