# -*- coding: utf-8 -*-

htmlStr = '''
<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=utf8'>
<HTML>
    <HEAD>
        <TITLE>TestCase Execution - Custom Report</TITLE>
        <STYLE>
            .textfont {font-weight: normal; font-size: 12px; color: #000000; font-family: verdana, arial, helvetica, sans-serif }
            .owner {width:100%%; border-right: #6d7683 1px solid; border-top: #6d7683 1px solid; border-left: #6d7683 1px solid; border-bottom: #6d7683 1px solid; background-color: #a3a9b1; padding-top: 3px; padding-left: 3px; padding-right: 3px; padding-bottom: 10px; }
            .product {color: white; font-size: 22px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: #59A699; padding: 5px 10px; border-top: 5px solid #a9b2c5; border-right: 5px solid #a9b2c5; border-bottom: #293f6f; border-left: 5px solid #a9b2c5;}
            .rest {color: white; font-size: 24px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: white; padding: 10px; border-right: 5px solid #a9b2c5; border-bottom: 5px solid #a9b2c5; border-left: 5px solid #a9b2c5 }
            .chl {font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; width: 17%%; height: 20px; border-bottom: 1px solid white }
            a {color: #336 }
            a:hover {color: #724e6d }
            .ctext {font-size: 11px; padding-right: 5px; padding-left: 5px; width: 80%%; height: 20px; border-bottom: 1px solid #eee }
            .hl {color: #724e6d; font-size: 12px; font-weight: bold; background-color: white; height: 20px; border-bottom: 2px dotted #a9b2c5 }
            .space {height: 10px;}
            h3 {font-weight: bold; font-size: 11px; color: white; font-family: verdana, arial, helvetica, sans-serif;}
            .tr_normal {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
            .tr_pass {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
            .tr_fail {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white; color: red;}
        </STYLE>
        <META content='MSHTML 6.00.2800.1106'>
    </HEAD>
    <body leftmargin='0' marginheight='0' marginwidth='0' topmargin='0'>
        <table width='100%%' border='0' cellspacing='0' cellpadding='0'>
            <tr>
                <td class='product'>Quality Center</td>
            </tr>
            <tr>
                <td class='rest'>
                    <table class='space' width='100%%' border='0' cellspacing='0' cellpadding='0'>
                        <tr>
                            <td></td>
                        </tr>
                    </table>                                                                        
                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                        <tbody>
                            <tr>
                                <td>
                                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                                        <tbody>
                                            <tr>
                                                <td class='chl' width='20%%'>Project Name</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>TotalCases</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>PassCases</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>FailCases</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>BeginTime</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>FinishTime</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td class='space'></td>
                            </tr>
                        </tbody>
                    </table>
                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                        <tbody>
                            <tr>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>Test</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>Name</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>Status</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>Count</td>
                            </tr>
                            %s
                        </tbody>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</HTML>'''

rowStr = '''
<tr>
    <td class='tr_normal'><a target='_blank' href='%s'>%s</a></td>
    <td class='tr_normal'>%s</td>
    <td class='tr_normal'>%s</td>
    <td class='tr_normal'>%s</td>
</tr>'''



def getRowStr(caseUrl,caseId,caseName,caseStatus,caseCount):
    return (rowStr %(caseUrl,caseId,caseName,caseStatus,caseCount))

def getHtmlStr(projecName,totalCase,passCase,failCase,start,end,totalRowStr):
    return (htmlStr %(projecName,totalCase,passCase,failCase,start,end,totalRowStr))