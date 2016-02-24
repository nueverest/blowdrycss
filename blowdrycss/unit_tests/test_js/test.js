/* References:
http://stackoverflow.com/questions/507138/how-do-i-add-a-class-to-a-given-element
http://www.w3schools.com/jquery/html_addclass.asp
http://www.w3schools.com/jquery/sel_class.asp
http://www.w3schools.com/jsref/met_document_getelementsbyclassname.asp
*/


// element.classList.add() variant 1
var element = document.getElementById("div1");
element.classList.add("addclass1");
// element.classList.add() variant 2
element.classList.add( 'addclass2' );

// element.classList.remove() variant 1
element.classList.remove("removeclass1");
// element.classList.remove() variant 2
element.classList.remove( 'removeclass2' );

// element.classList[] variant 1
var length = element.classList.length;
element.classList[length] = "arrayclass";
// element.classList[] variant 2
element.classList[length]='arrayclass';
// element.classList[] variant 3
var arrayclass = "arrayclass";
element.classList[length] = arrayclass;


var d = document.getElementById("div0");
// className variant 1
d.className += " padding-33";
// className variant 2
d.className+=' color-h111';
// className variant 3
var center = " text-align-center";
d.className += center;
// className variant 4
d.className += " padding-33 pink margin-left-5_5rem";
// className variant 5
d.className=d.className+' color-h111';
// className variant 6
d.className = d.className + ' color-h111';
// className variant 7
d.className = d.className + ' color-h111 bold green padding-10';


// Replace a class name variant 1
function toggleClass1 (El) {
    if (El.className != "white") {
        El.className = "white"
    }
    else{
        El.className = "black";
    }
}

// Replace a class name variant 2
function toggleClass2 (El) {
    if (El.className != 'white' ) {
        El.className = 'white'
    }
    else{
        El.className = 'black';
    }
}

// Replace a class name variant 3
function toggleClass3 (El) {
    var white = "white";
    var black = 'black';
    if (El.className != white) {
        El.className = white
    }
    else{
        El.className = black;
    }
}


function appendClass(elementId, classToAppend){
    var oldClass = document.getElementById(elementId).getAttribute("class");
    if (oldClass.indexOf(classToAdd) == -1)
    {
        // Test .setAttribute() as variable variant 1
        document.getElementById(elementId).setAttribute("class", classToAppend);
    }
}

// Test .setAttribute() as literal string variant 2
document.getElementById(elementId).setAttribute("class", "bold");
// Test .setAttribute() as literal string variant 3
document.getElementById(elementId).setAttribute( 'class','bold' );
// Test .setAttribute() as literal string variant 4
document.getElementById(elementId).setAttribute("class", "bold green padding-bottom-1_2rem");

// getElementByClassName variant 1
document.addEventListener('DOMContentLoaded', function() {
    document.getElementsByClassName('tabGroup')[0].className = "tabGroup ready";
});

// getElementByClassName variant 2
var x = document.getElementsByClassName("example");

// JQuery
$(document).ready( function() {
    var padding = "padding-top-10";
    $('#div1').addClass( 'font-size-35' );              // .addClass() variant 1
    $('#div2').addClass('blue');                        // .addClass() variant 2
    $('#div3').addClass("margin-top-50p");               // .addClass() variant 3
    $('#div4').addClass(padding);                       // .addClass() variant 4

    var a = document.body, c = ' classname';
    $(a).removeClass(c);                                // .removeClass() variant 1
    $(a).removeClass( "c-green" );                      // .removeClass() variant 2
    $(a).removeClass('c-blue');                         // .removeClass() variant 3

    var a_class = $(".class");                          // Class selector variant 1
    var bold = $('.bold');                              // Class selector variant 2
});


// YUI variant 1
YAHOO.util.Dom.addClass('div1','className');
// YUI variant 2
YAHOO.util.Dom.addClass('div2', "className" );
// YUI variant 3
YAHOO.util.Dom.addClass('div1',' className bold marging-top-5 ');
// YUI variant 4
YAHOO.util.Dom.hasClass(document.body,"classname");
// YUI variant 5
YAHOO.util.Dom.removeClass(document.body,"classname");


// Prototype variant 1
Element("document.body").ClassNames.add("classname");
// Prototype variant 2
Element("document.body").ClassNames.remove("classname");
// Prototype variant 3
Element("document.body").ClassNames.set("classname");
