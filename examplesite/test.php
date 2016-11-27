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

                            <ul>
                                <li>
                                    <div class="blue <?php echo $order_status; ?>">
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

                                <h4 style="text-align: left; padding-left: 60px;"><span class="hff9900">Color Codes Explained</span></h4>
                                <p style="text-align: left; padding-left: 60px;">
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
        $not_available = '<div class="margin-top-0 ' . $reader . '-not-available ' .
                         '"><a class=" ' .
                         '" href="#">Not Available</a></div>';
        $busy = '<div class="' . $reader . '-busy>' .
                '<a class="white  ' .
                '" href="#">Busy with Client</a></div>';

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