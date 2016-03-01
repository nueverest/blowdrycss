/* References:
http://stackoverflow.com/questions/507138/how-do-i-add-a-class-to-a-given-element
http://www.w3schools.com/jquery/html_addclass.asp
http://www.w3schools.com/jquery/sel_class.asp
http://www.w3schools.com/jsref/met_document_getelementsbyclassname.asp
https://dojotoolkit.org/reference-guide/1.7/dojo/addClass.html
https://dojotoolkit.org/reference-guide/1.7/dojo/removeClass.html
http://blog.sodhanalibrary.com/2014/08/add-class-remove-class-or-toggle-class.html#.Vs0eSNzm5f8
http://blog.sodhanalibrary.com/2016/02/add-class-remove-class-toggle-class-to.html#.Vs0fWtzm5f9 (angular 2)
*/


// create element
var element = document.getElementById("div1");
var notimplemented = " not implemented ";

// element.classList.add() variant 1
element.classList.add("addclass1");
// element.classList.add() variant 2
element.classList.add( "addclass2" );
// element.classList.add() variant 3
element.classList.add(
    "addclass3"
);
// element.classList.add() variant 4
element.classList.add('addclass4');
// element.classList.add() variant 5
element.classList.add( 'addclass5' );
// element.classList.add() variant 6
element.classList.add(
    'addclass6'
);
// className variables not implemented
element.classList.add(notimplemented);

// element.classList.remove() variant 1
element.classList.remove("removeclass1");
// element.classList.remove() variant 2
element.classList.remove( "removeclass2" );
// element.classList.remove() variant 3
element.classList.remove(
    "removeclass3"
);
// element.classList.remove() variant 4
element.classList.remove('removeclass4');
// element.classList.remove() variant 5
element.classList.remove( 'removeclass5' );
// element.classList.remove() variant 6
element.classList.remove(
    'removeclass6'
);
// className variables not implemented
element.classList.remove(notimplemented);

// Doesn't seem to work.
//// element.classList[] variant 1
//var length = element.classList.length;
//element.classList[length] = "arrayclass";
//// element.classList[] variant 2
//element.classList[length]='arrayclass';
//// element.classList[] variant 3
//var arrayclass = "arrayclass";
//element.classList[length] = arrayclass;


var d = document.getElementById("div0");
d.className = "className1";                                         // className variant 1
d.className="className2";                                           // className variant 2
d.className = " className3 ";                                       // className variant 3
d.className = "className4a className4b className4c";                // className variant 4
d.className = notimplemented;                                       // className variables not implemented

d.className = d.className + "className5";                           // className variant 5
d.className=d.className+"className6";                               // className variant 6
d.className = d.className + " className7 ";                         // className variant 7
d.className = d.className + "className8a className8b className8c";  // className variant 8
d.className = d.className + "className9a" + notimplemented;         // className variant 9 (only className9a extracted)
d.className = "className9b" + d.className + notimplemented;         // className variant 9 (only className9b extracted)
d.className=d.className+"className10"+notimplemented;               // className variant 10 (only className10 extracted)

d.className += "className11";                                       // className variant 11
d.className+="className12";                                         // className variant 12
d.className += " className13 ";                                     // className variant 13
d.className += "className14a className14b className14c";            // className variant 14
d.className += notimplemented + "className15" + notimplemented;     // className variant 15 (only className15 extracted)
d.className += notimplemented + "className16";                      // className variant 16 (only className16 extracted)
d.className+="className17"+notimplemented;                          // className variant 17 (only className17 extracted)
d.className += notimplemented;                                      // className variables not implemented


// Replace a class name variant 1
function toggleClass1 (El) {
    if (El.className != "white") {
        El.className = "className18";
    }
    else{
        El.className = "className19";
    }
}

// Replace a class name variant 2
function toggleClass2 (El) {
    if (El.className == 'blue' ) {                                  // TODO: This should not be returned by regex.
        El.className = 'className20';
    }
    else{
        El.className = 'className21';
    }
}

// Replace a class name NOT Implemented
function toggleClass3 (El) {
    var white = "green";
    if (El.className != white) {
        El.className = notimplemented;
    }
    else{
        El.className = notimplemented;
    }
}


function appendClass(elementId, classToAppend){
    var oldClass = document.getElementById(elementId).getAttribute("class");
    if (oldClass.indexOf(classToAdd) == -1)
    {
        // Test .setAttribute() as variable NOT Implemented
        document.getElementById(elementId).setAttribute("class", classToAppend);
    }
}

// getElementByClassName variant 22
document.addEventListener('DOMContentLoaded', function() {
    document.getElementsByClassName('tabGroup')[0].className = "className22";
});

// Test .setAttribute() as literal string variant 1
document.getElementById(elementId).setAttribute("class", "setAttribute1");
// Test .setAttribute() as literal string variant 2
document.getElementById(elementId).setAttribute( 'class','setAttribute2' );
// Test .setAttribute() as literal string variant 3
document.getElementById(elementId).setAttribute("class", "setAttribute3a setAttribute3b setAttribute3c");

// getElementByClassName variant 2
var x = document.getElementsByClassName("example");


// dojo

// Add a class dojo 1.7+ (AMD)
require(["dojo/dom-class"], function(domClass){
    domClass.add("example1", "style1");
});

// Add a class dojo < 1.7
dojo.addClass("example1", "style1");

// Add multiple dojo 1.7+ (AMD)
require(["dojo/dom-class"], function(domClass){
    domClass.add("example1", "style1 style2");
});

// Add mulitple dojo < 1.7
dojo.addClass("example1", "style1 style2");

// Remove a class. dojo 1.7+
require(["dojo/dom-class"], function(domClass){
    // Remove a class from some node:
    domClass.remove("someNode", "firstClass");
});

// Remove a class from some node:  dojo < 1.7
dojo.removeClass("someNode", "firstClass");

// Remove multiple classes dojo 1.7+ (AMD)
require(["dojo/dom-class"], function(domClass){
    domClass.remove("example1", "style1 style2");
});

// Remove multiple classes dojo < 1.7
dojo.removeClass("example1", "style1 style2");


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


// AngularJS variant 1
$scope.myClass = [];
$scope.myClass.push('red');
// AngularJS variant 2
$scope.myClass = [];
$scope.myClass.pop('red');
// AngularJS variant 3
$scope.myClass = ['red'];
if($scope.myClass.indexOf('red') == -1) {
    alert('false');
} else {
    alert('true');
}
// AngularJS variant 4
$scope.myClass = {red:false};
$scope.addClass = function() {
   $scope.myClass.red = true;
}
// AngularJS variant 5
$scope.myClass = {red:false};
$scope.removeClass = function() {
    $scope.myClass.red = false;
}
// AngularJS variant 6
$scope.myClass = {red:false};
$scope.toggleClass = function() {
     $scope.myClass.red = !$scope.myClass.red;
};
// AngularJS variant 7
$scope.myClass = {red:false};
$scope.toggleClass = function() {
     $scope.myClass.red = !$scope.myClass.red;
};
// AngularJS variant 8
var myEl8 = angular.element( document.querySelector( '#divID' ) );
myEl8.removeClass('red');
// AngularJS variant 9
var myEl9 = angular.element( document.querySelector( '#divID' ) );
myEl9.toggleClass('red');
// AngularJS variant 10
var myEl10 = angular.element( document.querySelector( '#divID' ) );
if(myEl10.hasClass('red')) {
  alert('has class red');
}