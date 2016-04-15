<%@ Page Title="" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="Default" %>
<%@ Register Src="~/uc/carousel/ucBlowDryerCarousel.ascx" TagPrefix="uc1" TagName="ucBlowDryerCarousel" %>


<asp:Content ID="Content1" ContentPlaceHolderID="HeadContent" Runat="Server"></asp:Content>

<%--Make Header and Navbar Full Width--%>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolderFullWidth" runat="server"></asp:Content>

<%--Remove Default Header--%>
<asp:Content ID="Content3" ContentPlaceHolderID="ContentPlaceHolderFront" Runat="Server">
    <div class=" row bgc-green padding-top-30 padding-bottom-30">
        Main Content<br />
        Padding is 30px top and bottom
        Background color is green.
    </div>

    <div Class='bgc-pink'>
        Class Capitalized<br>
        Single Quotes used
    </div>

    <%--Case Insensitivity Check + CssClass Check--%>
    <asp:LinkButton ID="lbTableContent1" runat="server" CssClass="color-h979591">Course Dashboard</asp:LinkButton>

    <div class="row padding-top-30 padding-bottom-30 <%=ClassSelector.Green %>">Is this green?</div>

    <div class="row padding-top-30 padding-bottom-30 <%=ClassSelector.Blue %>">Is this blue?</div>

    <div class="row padding-25-820-up <%#Eval("ProductName")%>"><uc1:ucBlowDryerCarousel runat="server" ID="ucBlowDryerCarousel" /></div>
</asp:Content>

<script>
    $(document).ready( function() {
        var padding = "not implemented";
        $('#div1').addClass( 'jquery1' );                   // .addClass() variant 1
        $('#div2').addClass('jquery2');                     // .addClass() variant 2
        $('#div3').addClass("jquery3");                     // .addClass() variant 4
        $('#div5').addClass('jquery4 jquery5');             // .addClass() variant 5
        $('#div6').addClass("jquery6 jquery7");             // .addClass() variant 6
        $('#div7').addClass(padding);                       // not implemented

        var a = document.body, c = ' not implemented';
        $(a).removeClass(c);                                // not implemented
        $(a).removeClass('jquery8');                        // .removeClass() variant 1
        $(a).removeClass('jquery9 jquery10');               // .removeClass() variant 2
        $(a).removeClass( "jquery11" );                     // .removeClass() variant 3
        $(a).removeClass( "jquery12 jquery13" );            // .removeClass() variant 4

        var bold = $('.jquery14');                          // Class selector variant 1
        var bol  = $( '.jquery15' );                        // Class selector variant 2
        var a_class = $(".jquery16");                       // Class selector variant 3
        var a_lass = $( ".jquery17" );                      // Class selector variant 4
    });
</script>
    

