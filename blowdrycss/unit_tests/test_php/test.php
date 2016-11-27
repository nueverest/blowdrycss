<?php /* Template Name: ReaderDashboard */ ?>

<style>
    .status {
        color: red;
    }

    .Completed {
        font-weight: bold;
        color: green;
    }

    .Processing {
        color: orange;
    }

    .Refunded {
        color: #6495ed;
    }
</style>

<!-- Foundation 6 CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/foundation/6.2.4/foundation.min.css">


<?php

global $wpdb;
$order_statuses = wc_get_order_statuses();

$current_path = get_current_path();                     // source: functions.php
$current_reader = $reader_paths[$current_path];

// Product ID - Cooresponds to reading service product.
$product_id = $current_reader['product_id'];

// Select all Orders for a Single Reading Product via order ID.
$sql_query = "SELECT order_id " .
             "WHERE meta_key = '_product_id' AND meta_value = %d " .
             "GROUP BY order_id;";

$order_ids = $wpdb->get_col( $wpdb->prepare( $sql_query, $product_id ) );

//foreach( $order_ids as $order_id ) {
//    var_dump($order_id);
//}

if( $order_ids ) {
    $args = array(
        'post_type' => 'shop_order',
        'post__in' => $order_ids,
        'post_status' => 'publish',
        'posts_per_page' => 2,
        'order' => 'DESC',
        'tax_query' => array(
            array(
                'taxonomy' => 'shop_order_status',
                'field' => 'slug',
                'terms' => array (
                    $order_statuses
                    //'Pending' , 'Failed' , 'Processing' , 'Completed', 'On-Hold' , 'Cancelled' , 'Refunded'
                )
            )
        )
    );
    $orders = new WP_Query( $args );
}

$reader_key = $current_reader['reader_key'];
$reader_busy_query = "SELECT `BusyWithClient` " .
                     "FROM {$wpdb->prefix}reader " .
                     "WHERE `Key`=%s";
$reader_busy = $wpdb->get_col( $wpdb->prepare( $reader_busy_query, $reader_key ) );

$reader_statuses = array(
    '0' => 'Available',                 // Default Manual Setting
    '1' => 'Busy with Client',          // Manual Setting
);

?>

<?php
    get_header();
?>

<div id="main-content" style="background-color: rgba(0,0,0,0.5);">

<?php while ( have_posts() ) : the_post(); ?>

	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>

		<div class="entry-content padding-bottom-80">

            <div class="row margin-top-75-i">
                <div class="small-12 columns">
                    <div class="et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_center"
                         style="font-family: 'Old Standard TT', Georgia, 'Times New Roman', serif;">
                        <h2>Dashboard for <?php echo $current_reader['full_name']; ?></h2>
                    </div> <!-- .et_pb_text -->

                    <hr style="border-color:#de9b17; margin:10px auto 30px auto;">
                </div>

                <div id="instructions" class="small-11 large-6 columns small-centered large-uncentered" style="margin-bottom: 40px;">
                    <div class="et_pb_text et_pb_module et_pb_bg_layout_dark et_pb_text_align_left et_pb_text_1"
                         style="padding-left:15px;">
                        <h2 style="color: #de9b17 !important; font-family: 'Old Standard TT', Georgia, 'Times New Roman', serif;">
                            After receiving a call:
                        </h2>

                        <ol>
                            <li>Instruct the querent to complete their payment online by selecting one of the payment buttons.</li>
                            <li style="margin-top: 13px;">First time customers&nbsp;need to register and fill out all payment information.</li>
                            <li style="margin-top: 13px;">Once the customer&nbsp;completes the payment. Click the golden refresh button.</li>
                            <li style="margin-top: 13px;">You should see a new <span class="Completed">GREEN</span> colored order matching the current time and date (Arizona Time).</li>
                            <li style="margin-top: 13px;">You can now start your timer based on the orders Reading Duration.</li>
                        </ol>
                    </div> <!-- .et_pb_text -->

                    <!-- Busy With Client -->
                    <div style="background-color: rgba(44,21,53,0.95); text-align: center; padding: 20px; border-radius: 5px; margin: 42px 0 60px 0;">
                        <h1>My Status</h1>
                        <h3 style="color:white;"><span id="busy"><?php echo available($reader_key); ?></span></h3>

                        <form id="toggleForm" method="post" action="">
                            <input class="button" style="font-size: 18px; padding: 10px; border-radius: 5px; margin: 20px 0px;"
                                   type="submit" name="toggle" value="Change Status" >
                        </form>
                    </div>

                    <!-- Countdown Timer -->
                    <div style="background-color: rgba(44,21,53,0.95); padding: 0px 20px 20px 20px; border-radius: 5px; margin: 30px 0 60px 0;">
                        <div style="padding: 20px;">
                            <h1 style="text-align: center; font-size: 32px; margin-bottom: 10px;">Reading Timer</h1>
                        </div>

                        <div style="text-align: center; padding: 20px;">
                            <span id="time" style="font-size: 42px; padding-right: 10px;">00:00</span> <span style="font-size: 42px; padding-right: 10px;">minutes</span>
                            <div style="font-weight: bold; margin-top: 15px;">
                                <button id="startTimer" style="padding:10px; background-color: green; color: white; border-radius: 3px;">Start Timer</button>
                            </div>

                            <div style="margin-top: 40px;">
                                <input id="minutes" type="number" value="15" style="width:75px; font-size: 26px; padding: 2px 5px 5px 5px; margin-bottom: 5px; display:inline-block;"> <span style="font-size: 26px; padding: 2px 5px 5px 5px;">minutes</span>
                                <div style="font-weight: bold; margin-top: 5px;">
                                    <button id="resetTimer" style="padding:10px; background-color: #6495ed; color: white; border-radius: 3px;">Reset Timer</button>
                                    <button id="setTimer" style="padding:10px; background-color: #de9b17; color: white; border-radius: 3px;">Set Timer</button>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <div class="small-12 large-6 columns"
                     style="background-color: rgba(0,0,0,0.5); text-align: left; color: white; padding: 12px; border-radius: 5px;">

                    <!-- Refresh Button -->
                    <div class="et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_center  et_pb_text_2"
                         style="margin-bottom: 30px;">
                        <div class="et_pb_button_module_wrapper et_pb_module">
                            <a class="et_pb_button et_pb_custom_button_icon et_pb_module et_pb_bg_layout_light pay-link" data-icon="" href="#" onclick="window.location.reload(true);"><span>Refresh Order List</span></a>
                        </div>
                    </div> <!-- .et_pb_text -->

                    <?php // Display products
                        if ($orders->have_posts()) :
                            while ($orders->have_posts()) :
                                $orders->the_post();
                                $order_id = $orders->post->ID;
                                $order = new WC_Order($order_id);

                                // Order Id / Date / Customer Name and more
                                $order_meta = get_post_meta($order_id);
                                $first_name = $order_meta['_billing_first_name'][0];
                                $last_name = $order_meta['_billing_last_name'][0];

                                // Status
                                $wc_order_status = $order->post->post_status;
                                $order_status = $order_statuses[$wc_order_status];

                                // Cost
                                $order_items = $order->get_items();
                    ?>

                    <div class="row">
                        <div class="small-10 medium-6 large-8 columns small-centered">
                            <ul>
                                <li>
                                    <div class="status <?php echo $order_status; ?>">
                                        <?php the_title(); ?>
                                    </div>

                                    <div>
                                        <?php print_r("Id: " . $order->id); ?>
                                    </div>

                                    <div>
                                        <?php
                                            foreach ( $order_items as $item ) {
                                                print_r("Amount Paid: $" . $order->get_line_total( $item ) );
                                            }
                                        ?>
                                    </div>

                                    <div>
                                        <?php
                                            foreach ( $order_items as $item ) {
                                                $unit_cost = $order->get_item_total( $item );
                                                $total_cost = $order->get_line_total( $item );
                                                $duration = $total_cost / $unit_cost;
                                                print_r("Reading Duration: " . $duration . ' minutes' );
                                            }
                                        ?>
                                    </div>

                                    <div>
                                        <?php print_r("Customer Name: " . $first_name . " " . $last_name); ?>
                                    </div>

                                    <div>
                                        <?php print_r("Payment: " . $order_status); ?>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                    <?php else:  ?>
                    <p>
                         <?php _e( 'No Orders' ); ?>
                    </p>
                    <?php endif; ?>

                    <div class="row">
                        <div class="small-10 medium-6 large-8 columns small-centered">
                            <div class="et_pb_text et_pb_module et_pb_bg_layout_dark et_pb_text_align_left  et_pb_text_3"
                                 style="margin-top: 30px;">
                                <h4 style="text-align: left; padding-left: 60px;"><span class="hff9900">Color Codes Explained</span></h4>
                                <p style="text-align: left; padding-left: 60px;">
                                    <strong><span class="Completed">Green</span></strong> – Completed<br>
                                    <span class="Processing">Orange</span> – Processing<br>
                                    <span class="Refunded">Blue</span> – Refunded<br>
                                    <span class="status">Red</span> – Pending, Cancelled, Failed
                                </p>
                            </div> <!-- .et_pb_text -->
                        </div>
                    </div>
                </div>
            </div>

            <?php
                the_content();
            ?>
        </div> <!-- .entry-content -->

	</article> <!-- .et_pb_post -->

<?php endwhile; ?>

</div> <!-- #main-content -->

<?php get_footer(); ?>

<!-- Foundation 6 JavaScript -->
<script src="https://cdn.jsdelivr.net/foundation/6.2.4/foundation.min.js"></script>


<script type="text/javascript">
    // Reference: http://stackoverflow.com/a/20618517/1783439
    function CountDownTimer(duration, granularity) {
      this.duration = duration;
      this.granularity = granularity || 1000;
      this.tickFtns = [];
      this.running = false;
    }

    CountDownTimer.prototype.start = function() {
      if (this.running) {
        return;
      }
      this.running = true;
      var start = Date.now(),
          that = this,
          diff, obj;

      (function timer() {
        diff = that.duration - (((Date.now() - start) / 1000) | 0);

        if (diff > 0) {
          setTimeout(timer, that.granularity);
        } else {
          diff = 0;
          that.running = false;
        }

        obj = CountDownTimer.parse(diff);
        that.tickFtns.forEach(function(ftn) {
          ftn.call(this, obj.minutes, obj.seconds);
        }, that);
      }());
    };

    CountDownTimer.prototype.onTick = function(ftn) {
      if (typeof ftn === 'function') {
        this.tickFtns.push(ftn);
      }
      return this;
    };

    CountDownTimer.prototype.expired = function() {
      return !this.running;
    };

    CountDownTimer.parse = function(seconds) {
      return {
        'minutes': (seconds / 60) | 0,
        'seconds': (seconds % 60) | 0
      };
    };

    window.onload = function () {
        var display = document.querySelector('#time'),
            minutes = document.getElementById('minutes');
            seconds = minutes.value * 60,
            timer = new CountDownTimer(seconds),
            timeObj = CountDownTimer.parse(seconds);

        format(timeObj.minutes, timeObj.seconds);

        timer.onTick(format);
        console.log('before startTimer() ' + timer.running);

        document.getElementById('startTimer').addEventListener('click', function () {
            console.log('inside startTimer event handler ' + timer.running);
            timer.start();
        });

        document.getElementById('resetTimer').addEventListener('click', function () {
            console.log('inside resetTimer event handler ' + timer.running);
            seconds = 0
            timer.duration = seconds;
            timeObj = CountDownTimer.parse(seconds);
            format(timeObj.minutes, timeObj.seconds);
        });

        document.getElementById('setTimer').addEventListener('click', function () {
            console.log('inside setTimer event handler ' + timer.running);
            seconds = minutes.value * 60;
            console.log('seconds ' + seconds);
            timer.duration = seconds;                   // Change timer duration
            timeObj = CountDownTimer.parse(seconds);
            format(timeObj.minutes, timeObj.seconds);
        });

        function format(minutes, seconds) {
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            display.textContent = minutes + ':' + seconds;
        }
    };

    // Handle form submission without reloading page: http://stackoverflow.com/a/20352888/1783439
    (function($) {
        $(document).ready( function() {
            var values = $(this).serialize();
            var toggleForm = $('#toggleForm');

            toggleForm.submit(function (e) {
                $.ajax({
                    url: "<?php echo 'https://thecleostore.com/busy/?reader_key=' . $reader_key ?>",
                    type: "post",
                    data: values ,
                    success: function (response) {
                        $("#busy").html(response);
                        console.log(response);
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log(textStatus, errorThrown);
                    }
                });
                e.preventDefault();
            });
        });
    })(jQuery);
</script>

<?php

// Phone Number Shortcode
// [reader_phone reader="gmg"]
function reader_phone_shortcode( $atts ) {
    $a = shortcode_atts( array(
        'reader' => '',
    ), $atts );

    $reader = $a['reader'];
    $reader_keys = get_reader_keys();
    $output = '';

    if(in_array($reader, $reader_keys)) {
        $phone_numbers = get_phone_numbers();
        $today = strtolower(day_of_week());
        $now = strtotime(now());
        $in = strtotime(reader_in($reader, $today));
        $out = strtotime(reader_out($reader, $today));

        manage_buttons($reader);

        $available = '<h2 style="text-align: center; color: #17de9b; font-weight: bold;">' .
                     $phone_numbers[$reader] . '</h2>';
        $not_available = '<div class="' . $reader . '-not-available et_pb_button_module_wrapper et_pb_module ' .
                         'et_pb_button_alignment_center margin-top-0"><a class="et_pb_button  et_pb_button_0 ' .
                         'et_pb_module et_pb_bg_layout_dark not-available" href="#">Not Available</a></div>';
        $busy = '<div class="' . $reader . '-busy et_pb_button_module_wrapper et_pb_module ' .
                'et_pb_button_alignment_center" style="margin-top: 0px;"><a class="white et_pb_button  et_pb_button_0 ' .
                'et_pb_module et_pb_bg_layout_dark busy" href="#">Busy with Client</a></div>';

        if($in <= $now && $now <= $out) {
            if(is_reader_busy($reader) == '0') {    // Reader Available
                $output = $available;
            }
            else {                                  // Reader Busy
                $output = $busy;
            }
        }
        else {                                      // Reader Not Available
            $output = $not_available;
        }
    }

    return $output;
}
add_shortcode( 'reader_phone', 'reader_phone_shortcode' );

//WC_Order Object (
//    [order_type] => simple
//    [id] => 126
//    [post] => WP_Post Object (
//        [ID] => 126
//        [post_author] => 1
//        [post_date] => 2016-11-13 08:29:00
//        [post_date_gmt] => 2016-11-13 15:29:00
//        [post_content] =>
//        [post_title] => Order – November 13, 2016 @ 08:29 AM
//        [post_excerpt] =>
//        [post_status] => wc-completed
//        [comment_status] => closed [ping_status] => closed
//        [post_password] =>
//        [post_name] => order-november-13-2016-0830-am
//        [to_ping] =>
//        [pinged] =>
//        [post_modified] => 2016-11-13 08:30:41
//        [post_modified_gmt] => 2016-11-13 15:30:41
//        [post_content_filtered] =>
//        [post_parent] => 0
//        [guid] => https://thecleostore.com/?post_type=shop_order&p=126
//        [menu_order] => 0
//        [post_type] => shop_order
//        [post_mime_type] =>
//        [comment_count] => 1
//        [filter] => raw
//    )
//    [order_date] => 2016-11-13 08:29:00
//    [modified_date] => 2016-11-13 08:30:41
//    [customer_message] =>
//    [customer_note] =>
//    [post_status] => wc-completed
//    [prices_include_tax] =>
//    [tax_display_cart] => excl
//    [display_totals_ex_tax] => 1
//    [display_cart_ex_tax] => 1
//    [formatted_billing_address:protected] =>
//    [formatted_shipping_address:protected] =>
//    [billing_email] => nu.everest@gmail.com
//)
?>