# python 2
from __future__ import absolute_import, print_function, unicode_literals, with_statement
import _thread

# builtins
from unittest import TestCase, main
import logging
import sys
from io import StringIO, open
from time import sleep
from os import path, remove

# plugins
from blowdrycss.utilities import unittest_file_path, change_settings_for_testing, make_directory, delete_file_paths
from blowdrycss import watchdogwrapper
import blowdrycss_settings as settings

change_settings_for_testing()


class TestWatchdogWrapperMain(TestCase):
    passing = True
    non_matching = ''
    output = ''

    def monitor_modify_delete_stop(self, file_path):
        """ Monitor console output. Modify the file to trigger watchdog on_modified().
        Delete file at file_path_to_delete. Wait for output. Stop watchdogwrapper.main()
        Reference: http://stackoverflow.com/questions/7602120/sending-keyboard-interrupt-programmatically

        """
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
        ]

        saved_stdout = sys.stdout           # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            # Wait for main() to start.
            while 'Ctrl + C' not in out.getvalue():
                sleep(0.05)

            # Modify file
            with open(file_path, 'w') as generic_file:
                generic_file.write('<html>modified</html>')

            # IMPORTANT: Must wait up to 5 seconds for output otherwise test will fail.
            count = 0
            while substrings[-1] not in out.getvalue():
                if count > 100:             # Max wait is 5 seconds = 100 count * 0.05 sleep
                    break
                else:
                    sleep(0.05)
                    count += 1

            output = out.getvalue()

            for substring in substrings:
                if substring not in output:
                    self.passing = False
                    self.non_matching = substring
                    self.output = output
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout
            remove(file_path)               # Remove html file.
            _thread.interrupt_main()        # Stop watchdogwrapper.main().

    def monitor_limit_expires_stop(self):
        """ Monitor console output. Wait for output based on LimitTimer expiration. Stop watchdogwrapper.main()
        Reference: http://stackoverflow.com/questions/7602120/sending-keyboard-interrupt-programmatically

        """
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
            '----- Limit timer reset -----',
        ]

        saved_stdout = sys.stdout           # Monitor console
        try:
            out = StringIO()
            sys.stdout = out

            # Wait for main() to start.
            while 'Ctrl + C' not in out.getvalue():
                sleep(0.05)

            # IMPORTANT: Must wait up to 5 seconds for output otherwise test will fail.
            count = 0
            while substrings[-1] not in out.getvalue():
                if count > 100:             # Max wait is 5 seconds = 100 count * 0.05 sleep
                    break
                else:
                    sleep(0.05)
                    count += 1

            output = out.getvalue()

            for substring in substrings:
                if substring not in output:
                    self.passing = False
                    self.non_matching = substring
                    self.output = output
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout
            _thread.interrupt_main()        # Stop watchdogwrapper.main().

    def test_main_auto_generate_True_on_modify(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        html_text = '<html></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        test_css = unittest_file_path(folder='test_examplesite/test_css')
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        make_directory(test_css)
        self.assertTrue(path.isdir(test_examplesite))
        self.assertTrue(path.isdir(test_css))

        # Create file delete.html
        with open(delete_dot_html, 'w') as _file:
            _file.write(html_text)

        # Double check to ensure it got created.
        self.assertTrue(path.isfile(delete_dot_html))

        auto_generate = settings.auto_generate          # original
        settings.auto_generate = True
        _thread.start_new_thread(self.monitor_modify_delete_stop, (delete_dot_html,))
        sleep(0.25)               # Required for Travis CI
        watchdogwrapper.main()    # Caution: Nothing will run after this line unless _thread.interrupt_main() is called.
        self.assertTrue(self.passing, msg=self.non_matching + ' not found in output:\n' + self.output)
        settings.auto_generate = auto_generate          # reset setting

    def test_main_auto_generate_True_limit_timer_expired(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        html_text = '<html><div class="blue"></div></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        test_css = unittest_file_path(folder='test_examplesite/test_css')
        limit_dot_html = unittest_file_path(folder='test_examplesite', filename='limit_expired.html')

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        make_directory(test_css)
        self.assertTrue(path.isdir(test_examplesite))
        self.assertTrue(path.isdir(test_css))

        # Create file limit_expired.html
        with open(limit_dot_html, 'w') as _file:
            _file.write(html_text)

        # Double check to ensure it got created.
        self.assertTrue(path.isfile(limit_dot_html))

        auto_generate = settings.auto_generate              # original
        time_limit = settings.time_limit

        settings.auto_generate = True
        settings.time_limit = 0.1                           # reduce the time_limit
        _thread.start_new_thread(self.monitor_limit_expires_stop, ())
        watchdogwrapper.main()    # Caution: Nothing will run after this line unless _thread.interrupt_main() is called.
        self.assertTrue(self.passing, msg=self.non_matching + ' not found in output:\n' + self.output)

        remove(limit_dot_html)                              # delete files
        settings.auto_generate = auto_generate              # reset setting
        settings.time_limit = time_limit

    def test_main_auto_generate_False_print_statements(self):
        # Integration test
        logging.basicConfig(level=logging.DEBUG)
        substrings = [
            '~~~ blowdrycss started ~~~',
            'Auto-Generated CSS',
            'Completed',
            'blowdry.css',
            'blowdry.min.css',
        ]
        html_text = '<html></html>'
        test_examplesite = unittest_file_path(folder='test_examplesite')
        test_css = unittest_file_path(folder='test_css')
        delete_dot_html = unittest_file_path(folder='test_examplesite', filename='delete.html')
        auto_generate = settings.auto_generate              # original

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        make_directory(test_css)
        self.assertTrue(path.isdir(test_examplesite))
        self.assertTrue(path.isdir(test_css))

        # Create delete.html
        with open(delete_dot_html, 'w') as _file:
            _file.write(html_text)

        self.assertTrue(path.isfile(delete_dot_html))

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            settings.auto_generate = False
            watchdogwrapper.main()

            sleep(0.25)                                     # IMPORTANT: Must wait for output otherwise test will fail.

            output = out.getvalue()

            for substring in substrings:
                self.assertTrue(substring in output, msg=substring + '\noutput:\n' + output)
        finally:
            sys.stdout = saved_stdout
            remove(delete_dot_html)                         # Delete delete.html
            settings.auto_generate = auto_generate          # reset setting

    def test_main_auto_generate_False_css_text_Fully_Integrated_Test(self):
        # Integration test that checks blowdry.css and blowdry.min.css output.
        logging.basicConfig(level=logging.DEBUG)
        expected_css_text = """.h444-hover:hover {
    color: #444
    }
.height-200 {
    height: 12.5em
    }
.talign-center {
    text-align: center
    }
.bgc-h000 {
    background-color: #000
    }
.fantasy {
    font-family: fantasy
    }
.padding-5 {
    padding: 0.3125em
    }
.c-blue {
    color: blue
    }
.display-none {
    display: none
    }
.t-align-center {
    text-align: center
    }
.padding-top-10 {
    padding-top: 0.625em
    }
.rgb-255-255-255 {
    color: rgb(255, 255, 255)
    }
.margin-top-30 {
    margin-top: 1.875em
    }
.bold {
    font-weight: bold
    }
.border-1px-solid-gray {
    border: 1px solid gray
    }
.sans-serif {
    font-family: sans-serif
    }
.height-150px {
    height: 9.375em
    }
.margin-top-10 {
    margin-top: 0.625em
    }
.border-5px-solid-hd0d {
    border: 5px solid #d0d
    }
.color-hfff {
    color: #fff
    }
.hfff-hover-i:hover {
    color: #fff !important
    }
.margin-top-50px {
    margin-top: 3.125em
    }
.display-inline {
    display: inline
    }
.red-i-hover:hover {
    color: red !important
    }
.margin-20 {
    margin: 1.25em
    }
.orange {
    color: orange
    }
.margin-25 {
    margin: 1.5625em
    }
.bgc-hf8f8f8 {
    background-color: #f8f8f8
    }
.h484848 {
    color: #484848
    }
.padding-10 {
    padding: 0.625em
    }
.width-50 {
    width: 3.125em
    }
.text-align-center {
    text-align: center
    }
.bgc-h5f2424-i-hover:hover {
    background-color: #5f2424 !important
    }
.width-150 {
    width: 9.375em
    }
.height-50px {
    height: 3.125em
    }
.padding-100-s {
    padding: 6.25em
    }
@media only screen and (max-width: 64em) {
    .padding-100-s {
        padding: 5.9923em
        }
    }
@media only screen and (max-width: 45em) {
    .padding-100-s {
        padding: 5.5556em
        }
    }
@media only screen and (max-width: 30em) {
    .padding-100-s {
        padding: 5em
        }
    }
@media only screen and (max-width: 45.0625em) {
    .large-up {
        display: none
        }
    }
@media only screen and (max-width: 45em) {
    .display-720-up {
        display: none
        }
    }
.font-size-48-s {
    font-size: 3em
    }
@media only screen and (max-width: 64em) {
    .font-size-48-s {
        font-size: 2.8763em
        }
    }
@media only screen and (max-width: 45em) {
    .font-size-48-s {
        font-size: 2.6667em
        }
    }
@media only screen and (max-width: 30em) {
    .font-size-48-s {
        font-size: 2.4em
        }
    }
@media only screen and (max-width: 30.0625em) {
    .display-medium-up {
        display: none
        }
    }
@media only screen and (min-width: 45.0625em) and (max-width: 64em) {
    .padding-100-large-only {
        padding: 6.25em
        }
    }
.font-size-48-s-i {
    font-size: 3em !important
    }
@media only screen and (max-width: 64em) {
    .font-size-48-s-i {
        font-size: 2.8763em !important
        }
    }
@media only screen and (max-width: 45em) {
    .font-size-48-s-i {
        font-size: 2.6667em !important
        }
    }
@media only screen and (max-width: 30em) {
    .font-size-48-s-i {
        font-size: 2.4em !important
        }
    }"""
        expected_css_min_text = ".h444-hover:hover{color:#444}.height-200{height:12.5em}" \
            ".talign-center{text-align:center}" \
            ".bgc-h000{background-color:#000}.fantasy{font-family:fantasy}.padding-5{padding:.3125em}" \
            ".c-blue{color:blue}.display-none{display:none}.t-align-center{text-align:center}" \
            ".padding-top-10{padding-top:.625em}.rgb-255-255-255{color:rgb(255,255,255)}" \
            ".margin-top-30{margin-top:1.875em}.bold{font-weight:bold}" \
            ".border-1px-solid-gray{border:1px solid gray}.sans-serif{font-family:sans-serif}" \
            ".height-150px{height:9.375em}.margin-top-10{margin-top:.625em}" \
            ".border-5px-solid-hd0d{border:5px solid #d0d}.color-hfff{color:#fff}" \
            ".hfff-hover-i:hover{color:#fff !important}.margin-top-50px{margin-top:3.125em}" \
            ".display-inline{display:inline}.red-i-hover:hover{color:red !important}" \
            ".margin-20{margin:1.25em}" \
            ".orange{color:orange}.margin-25{margin:1.5625em}.bgc-hf8f8f8{background-color:#f8f8f8}" \
            ".h484848{color:#484848}.padding-10{padding:.625em}.width-50{width:3.125em}" \
            ".text-align-center{text-align:center}" \
            ".bgc-h5f2424-i-hover:hover{background-color:#5f2424 !important}.width-150{width:9.375em}" \
            ".height-50px{height:3.125em}.padding-100-s{padding:6.25em}" \
            "@media only screen and (max-width:64em){.padding-100-s{padding:5.9923em}}" \
            "@media only screen and (max-width:45em){.padding-100-s{padding:5.5556em}}" \
            "@media only screen and (max-width:30em){.padding-100-s{padding:5em}}" \
            "@media only screen and (max-width:45.0625em){.large-up{display:none}}" \
            "@media only screen and (max-width:45em){.display-720-up{display:none}}" \
            ".font-size-48-s{font-size:3em}@media only screen and (max-width:64em){" \
            ".font-size-48-s{font-size:2.8763em}}@media only screen and (max-width:45em){" \
            ".font-size-48-s{font-size:2.6667em}}@media only screen and (max-width:30em){" \
            ".font-size-48-s{font-size:2.4em}}@media only screen and (max-width:30.0625em){" \
            ".display-medium-up{display:none}}@media only screen and (min-width:45.0625em) and " \
            "(max-width:64em){.padding-100-large-only{padding:6.25em}}.font-size-48-s-i{" \
            "font-size:3em !important}@media only screen and (max-width:64em){.font-size-48-s-i{" \
            "font-size:2.8763em !important}}@media only screen and (max-width:45em){.font-size-48-s-i{" \
            "font-size:2.6667em !important}}@media only screen and (max-width:30em){.font-size-48-s-i{" \
            "font-size:2.4em !important}}"
        html_text = """<html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>blowdrycss - example site</title>
                <link rel="icon" type="image/x-icon" href="images/favicon.ico">
                <link rel="stylesheet" type="text/css" href="css/blowdry.min.css" />
            </head>

            <body>
                <!-- Title -->
                <h1 class="c-blue hfff-hover-i bgc-h5f2424-i-hover text-align-center display-medium-up font-size-48-s">
                    Blow Dry CSS
                </h1>
                <div>
                    <img src="images/why-blow-dry.jpg" alt="Blow Dry CSS" title="Blow Dry CSS" width=480 />
                </div>

                <div class="t-align-center margin-top-50px large-up">
                    <img class="width-150 height-150px" src="images/blow.jpg" alt="blow" title="blow" />
                    <img class=" width-50 height-50px" src="images/plus.png" alt="plus" title="plus" />
                    <img class="width-150 height-150px" src="images/dry-ground.jpg" alt="dry" title="dry" />
                    <img class=" width-50 height-50px" src="images/plus.png" alt="plus" title="plus" />
                    <img class="width-150 height-150px" src="images/css.jpg" alt="css" title="css" />
                </div>

                <!-- Blow Dryers -->
                <ul class="margin-top-10">
                    <li class="bold padding-top-10">
                        <div>
                            <img class="height-200" src="images/blow-dryer1.jpg" alt="hair-yer1" title="blow-dryer1" />
                        </div>
                        <div class="color-hfff bgc-h000 padding-100-large-only">
                            A blow dryer drys the dryer of the hair.
                            <br class="display-none" />
                            This should be on the same line i.e. br-tag should be hidden once css is applied.
                        </div>
                    </li>

                    <li class="font-size-48-s-i padding-top-10">
                        <div>
                            <img class="height-200" src="images/blow-dryer2.jpg" alt="hadryer2" title="blow-dryer2" />
                        </div>
                        <div class="h484848 bgc-h000">
                            A blow dryer drys the hair of the dryer of hair.
                        </div>
                    </li>

                    <li class="b padding-top-10">
                        <div>
                            <img class="height-200" src="images/blow-dryer3.jpg" alt="ha-dryer3" title="blow-dryer3" />
                        </div>
                        <div class="color-#fff bgc-#000">
                            A blow dryer drys the dryer of hair. Intentional WRONG HEX ENCODING
                        </div>
                    </li>

                    <li class="b padding-top-10 h444-hover">
                        <div class="">
                            <img class="height-200 border-5px-solid-hd0d" src="images/blow-dryer4.jpg" />
                        </div>
                        <div class="rgb-255-255-255 bgc-h000">
                            <h3 class="sans-serif">
                                A blow dryer <span class="fantasy orange">drys</span> the dryer of hair.
                            </h3>
                        </div>
                    </li>
                </ul>

                <div class="hfff h000000-hover">Testing</div>

                <!-- <p class="margin-left-123">Class should not be found in comments</p> -->
                <h1 class="c-blue  text-align-center padding-10 display-720-up">Blow Dry CSS</h1>
                <div id="div1">Should have margin of 25px all the way around. Javascript class selectors.</div>
                <div class="padding-100-s margin-20 red-i-hover margin-top-30 border-5px-solid-hd0d">
                    Testing<br class="hide" />1 2 3
                </div>

                <script>
                    // create element
                    var element = document.getElementById("div1");
                    // element.classList.add() variant 1
                    element.classList.add("margin-25");
                </script>
            </body>
        </html>"""
        test_examplesite = unittest_file_path(folder='test_examplesite')
        test_css = unittest_file_path(folder='test_examplesite/test_css')
        blowdry_css = unittest_file_path(folder=test_css, filename='blowdry.css')
        blowdry_min_css = unittest_file_path(folder=test_css, filename='blowdry.min.css')
        test_dot_html = unittest_file_path(folder='test_examplesite', filename='test.html')
        auto_generate = settings.auto_generate                                                      # original

        # Directory must be created for Travis CI case
        make_directory(test_examplesite)
        make_directory(test_css)
        self.assertTrue(path.isdir(test_examplesite))
        self.assertTrue(path.isdir(test_css))

        # Create delete.html
        with open(test_dot_html, 'w') as _file:
            _file.write(html_text)

        self.assertTrue(path.isfile(test_dot_html))

        settings.auto_generate = False
        watchdogwrapper.main()
        sleep(0.25)

        # Human-readable CSS
        with open(blowdry_css, 'r') as css_text:
            self.assertTrue(expected_css_text, css_text.read())

        # Minified CSS
        with open(blowdry_min_css, 'r') as css_min_text:
            self.assertTrue(expected_css_min_text, css_min_text.read())

        delete_file_paths((test_dot_html, blowdry_css, blowdry_min_css, ))                          # Delete test html
        settings.auto_generate = auto_generate                                                      # reset setting


if __name__ == '__main__':
    main()

