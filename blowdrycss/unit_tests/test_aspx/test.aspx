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

    <div class="row padding-top-30 padding-bottom-30 <%=ClassSelector.Green %>">Is this green?</div>

    <div class="row padding-top-30 padding-bottom-30 <%=ClassSelector.Blue %>">Is this blue?</div>

    <div class="row <%#Eval("ProductName")%>"><uc1:ucBlowDryerCarousel runat="server" ID="ucBlowDryerCarousel" /></div>
</asp:Content>
    

