using System;
using System.Collections;
using System.Data;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Diagnostics;
using System.Web.Configuration;
using System.Text.RegularExpressions;
using System.Web.UI.HtmlControls;

public partial class individual_courses_courseplay : System.Web.UI.Page
{
    private void DisplayChapterOverall(string strAutoPlay)
    {
        DisplaySectionList();        // Set the next hidden url field.

        Hashtable hsParam = new Hashtable();
        hsParam.Add("CourseId", hdCourseId.Value);
        hsParam.Add("ChapterId", hdChapterId.Value);
        hsParam.Add("SectionId", hdSectionId.Value);
        hsParam.Add("CustomerId", User.Identity.Name);        
        hsParam.Add("UpdatedIP", Request.UserHostAddress); 
        DataTable dt = DbHelper.GetDataTableSp("up_courseContentChapter_Overall", hsParam); //Section Progress is updated too in this query.
        
        if (dt.Rows.Count > 0)
        {
            // Previous Button
            if (hdPreviousCourseUrl.Value.Contains("/") == false && (dt.Rows[0]["prevChapterUrl"].ToObjectString() != ""))
            {
                hdPreviousCourseUrl.Value = dt.Rows[0]["prevChapterUrl"].ToObjectString();  // First section of Next Chapter
            }

            if (hdPreviousCourseUrl.Value.Contains("/"))   
            {       
                PreviousLargeUp.Text = (
                    "<a href='" + hdPreviousCourseUrl.Value + "' onclick='Previous_Clicked' title='" + dt.Rows[0]["prevChapterSEO"].ToObjectString() + "' class='font-size-14'>" +
                        "<div class='large-up'>" +
                            "<i class='padding-bottom-2'>&#xE5CB;</i>Previous" +
                        "</div>" +
                    "</a>"                   
                );

                PreviousMediumDown.Text = (
                    "<a href='" + hdPreviousCourseUrl.Value + "' onclick='Previous_Clicked' title='" + dt.Rows[0]["prevChapterSEO"].ToObjectString() + "' class='white-hover'>" +
                        "<div class='hide small-6 columns border-right-width-2'>" +
                            "<i class='material-icons vertical-align-middle padding-bottom-2'>&#xE5CB;</i>Previous" +
                        "</div>" +
                    "</a>"    
                );
            }

            // Next Button
            if (hdNextCourseUrl.Value.Contains("/") == false && (dt.Rows[0]["nextChapterUrl"].ToObjectString() != ""))
            {
                hdNextCourseUrl.Value = dt.Rows[0]["nextChapterUrl"].ToObjectString();  // First section of Next Chapter
            }
            
            if (hdNextCourseUrl.Value.Contains("/"))                                    // Assign next section to hyperlink.
            {
                Debug.Write("\nhdNextCourseUrl.Value: " + hdNextCourseUrl.Value);
                NextLargeUp.Text = (
                    "<a id='NextLargeUp' runat='server' href='" + hdNextCourseUrl.Value + "' onclick='Next_Clicked' title='" + dt.Rows[0]["nextChapterSEO"].ToObjectString() + "' class='incorrect-class-25'>" +
                        "<div class='large-up large-3 xlarge-2 columns'>" +
                            "Next<i class='material-icons vertical-align-middle padding-bottom-2'>&#xE5CC;</i>" +
                        "</div>" +
                    "</a>"
                );

                NextMediumDown.Text = (
                    "<a id='NextMediumDown' runat='server' href='" + hdNextCourseUrl.Value + "' onclick='Next_Clicked' title='" + dt.Rows[0]["nextChapterSEO"].ToObjectString() + "' class='squirrel'>" +
                        "<div class='padding-bottom-17'>" +
                            "Next<i class='material-icons vertical-align-middle padding-bottom-2'>&#xE5CC;</i>" +
                        "</div>" +
                    "</a>"
                );
            }

            if (Convert.ToBoolean(dt.Rows[0]["currIsVideo"].ToString())) //If it is a video section, always display section list.
            {
                lbDisplayVideo.Visible = true;
                continuousPlayDiv.Visible = true;       //pnPlayControl.Visible = true;
                lbDisplayOther.Visible = false;
                pnContentList.Visible = true;

                string strVideoCd = dt.Rows[0]["currVideoCd"].ToObjectString();

                // CssClass Pattern source: http://stackoverflow.com/questions/3742010/add-css-class-to-a-div-in-code-behind
                continuousPlayDiv.CssClass="orange";
                continuousPlayDiv.CssClass = strVideoCd + ' h000 ';
                continuousPlayDiv.CssClass = " margin-top-10 margin-bottom-72 ";

                // .Attributes.Add("class", ...) cases
                BtnventCss.Attributes.Add("class", "pink");
                BtnventCss.Attributes.Add(
                    "class",
                    "xsmall-only"
                );
                BtnventCss.Attributes.Add( "class", strVideoCd + ' height-12 ' );
                BtnventCss.Attributes.Add("class"," width-100p inline ");

                if (strVideoCd != "Coming Soon")
                {
                    lbDisplayVideo.Text = (
                        // Test inline comment.
                        // "<div class='flex-video widescreen vimeo margin-bottom-0'>" +

                            // Contrived string concatenation NOT HANDLED
                            "<iframe class='" + "vimeo xlarge-only" + "' id='player1' src='//player.vimeo.com/video/"


                                + strVideoCd
                                + "?api=1&player_id=player1&autoplay="
                                + strAutoPlay
                                + "' frameborder='0' webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>" +
                        "</div>"
                    );
                }
                else
                {
                /*  Test block comment
                    lbDisplayVideo.Text = (
                        "<div class='flex-video widescreen vimeo'><div class='margin-top-20 b'><div class='font-size-20 bold'>Coming Soon</div><img src='"
                        + Source.CloudRoot + dt.Rows[0]["bannerFile"].ToObjectString()
                        + "' /></div></div>"
                    );
                */
                }
                //ltrSectionDescription.Text = dt.Rows[0]["currSectionDescription"].ToObjectString();
            }
            else if (dt.Rows[0]["relatedSectionNum"].ToString() == "1") //If it is a non-video section and only one section under this chapter, hide section list.
            {
                lbDisplayVideo.Visible = false;
                continuousPlayDiv.Visible = false;  //pnPlayControl.Visible = false;
                lbDisplayOther.Visible = true;
                Source source = new Source();
                lbDisplayOther.Text = source.AddCloudRoot(dt.Rows[0]["currDisplayContent"].ToObjectString());
                pnContentList.Visible = false;
            }
            else //If it is a non-video section but there are more than one section under this chapter, display section list.
            {
                lbDisplayVideo.Visible = false;
                lbDisplayOther.Visible = true;
                lbDisplayOther.Text = dt.Rows[0]["currDisplayContent"].ToObjectString();
                pnContentList.Visible = true;
            }
        }

        lbTableContent1.PostBackUrl = "/courses/contents/" + hdCourseId.Value + "/" + hdCourseUrl.Value;
        //lbTableContent2.PostBackUrl = lbTableContent1.PostBackUrl;


    }
