#!/usr/bin/python
import csv, sys, getopt, os, urllib2, re, glob
from bs4 import BeautifulSoup

# html page processing function
def processData(pageFile, out):
    ''' take the data from an html file and append to our csv file '''
    f = open(pageFile, "r")
    page = f.read()
    f.close()
    soup = BeautifulSoup(page)
    
    # Comment info
    posts = []
    authors = []
    times = []
    
    # Header info
    victimName = []
    victimAge = []
    victimLocation = []
    description = []
    uploadDate = []
    pageviews = []
    description = []
    
    # extract comment data
    for html in soup.findAll("div", { "class" : "trimbox" }):
        for commentbody in html.findAll("div", { "class" : "comment-body" }): 
            if len(commentbody.findAll("p")) > 0:
                posts.append(' '.join([p.contents[0].encode('utf-8') for p in commentbody.findAll("p")]))
            else:
                print "WARNING: Comment found with no text"
                posts.append('')
        for cite in html.findAll("cite", { "class" : "fn" }):
            authors.append(cite.contents[0])
        for commentmetadata in html.findAll("div", { "class" : "comment-meta commentmetadata" }):
            times.append(commentmetadata.find("a").contents[0].strip())
   
    # extract header data and create array length of comments
    for html in soup.findAll("div", { "class" : "profilehead" }):
        viewsAndDate = html.find("div", { "class" : "views" } ).text
        reDate = re.compile(r'(?<=Added )(.{12})')
        reViews = re.compile(r'(\d{1,10})(?= Views)')
        reAge = re.compile(r'\d{1,3}(?=\s+years old)')
        reLoc = re.compile(r'(?<=years old)\s+in\s+([()\w\s-]+,[()\w\s-]+)')
        try:
            uploadDate = [re.search(reDate, viewsAndDate).group(0)]*len(posts)
        except:
            pass
        try:
            pageviews = [re.search(reViews, viewsAndDate).group(0)]*len(posts)  
        except:
            pass
        try:
            victimName = [html.find("h1").text]*len(posts)
        except:
            pass
        try:
            victimAge = [re.search(reAge, re.sub('\s+',' ',html.text)).group(0)]*len(posts)
        except:
            pass
        try:
            victimLocation = [re.search(reLoc, re.sub('\s+',' ',html.text)).group(1)]*len(posts)
        except:
            pass
    
    for html in soup.findAll("div", { "class" : "profilecontent"}):
        description = [re.sub('\s+',' ',html.text)]*len(posts)
    
    csvfile = open(out, 'ab')
    writer = csv.writer(csvfile)

    # iterate through and write all the data
    for time, author, post, date, name, age, loc, description, views in zip(times, authors, posts, uploadDate, victimName, victimAge, victimLocation, description, pageviews):
        row = [time, author, post, date, name, age, loc, description, views]
        writer.writerow([col.encode('utf-8') for col in row])

    # close file
    csvfile.close()
    

def main(argv):
    dir = ''
    csvFile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["dir=","csvFile="])
    except getopt.GetoptError:
        print 'test.py -i <dir> -o <csvFile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <dir> -o <csvFile>'
            sys.exit()
        elif opt in ("-i", "--dir"):
            dir = arg
        elif opt in ("-o", "--csvFile"):
            csvFile = arg

    # insert the column titles to csv
    csvfile = open(csvFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Author", "Post", "Upload Date", "Victim Name", "Age", "Location", "Description", "Page Views"])
    csvfile.close()

    # get a list of files in the directory
    fileList = glob.glob(dir+"/*.html")

    # define variables we need for status text
    totalLen = len(fileList)
    count = 1

    # iterate through files and read all of them into the csv file
    for htmlFile in fileList:
        processData(htmlFile, csvFile) # process the data in the file
        print "Processed '" + htmlFile + "'(" + str(count) + "/" + str(totalLen) + ")..." # display status
        count = count + 1 # incriment counter

if __name__ == "__main__":
    main(sys.argv[1:])
    
# Header EXAMPLE
# <div class="profilehead">
#     <!-- name age location -->	
#     <div class="views">
#         <div  class="btnRemove">
#             <a href="http://removemanager.com/myex/" target="_blank">
#                 <img src="http://www.myex.com/wp-content/themes/MyEXTheme/images/removeyn.png" />
#             </a>
#         </div>
#         Added Jul 19, 2014				<br />
#                                             26009 Views
#     </div>
#     <h1>Aide  Badilla</h1>
#     26  years old in Timmins, Canada					
#     <!-- /name age location -->				
# </div>
# <!-- /profilehead -->			   
# <div class="profilecontent">
# 	<h2 class="extitle">"Aide Badilla"</h2>
#     <p>BLAH BLAH BLAH</b></p>
# </div>


# Comment EXAMPLE
# <!-- comments -->				
# <div id="profileCommentary">
# 	<!--- COMMENT PANEL --->
# 	<h2>COMMENTS<br />
# 	    <span class="tag">Do not post phone numbers or addresses</span>
# 	</h2>
# 	<div class="trimbox">		
#         <!-- You can start editing here. -->
#         <div id="commentsbox">
# 	        <h3 id="comments">11 Responses so far...</h3>
#             <ol class="commentlist">
# 			    <li class="comment even thread-even depth-1" id="comment-102468">
# 				    <div id="div-comment-102468" class="comment-body">
# 				        <div class="comment-author vcard">
# 			                <img alt='' src='http://1.gravatar.com/avatar/dd8889793c4d9e43e26949e5f6e68072?s=32&amp;d=http%3A%2F%2F1.gravatar.com%2Favatar%2Fad516503a11cd5ca435acc9bb6523536%3Fs%3D32&amp;r=G' class='avatar avatar-32 photo' height='32' width='32' />			
# 			                <cite class="fn">Mickey05</cite> 
# 			                <span class="says">says:</span>		
# 			            </div>
# 		                <div class="comment-meta commentmetadata">
# 		                    <a href="http://www.myex.com/ex/aide-badilla/#comment-102468">
# 			July 20, 2014 at 12:35 am
# 			                </a>		
# 			            </div>
# 		                <p>Check myex.com/ile-de-france/versailles/annabelle-barr/19486/<br />
# She&#8217;s on Facebook at facebook.com/annabelle.barre</p>
#                         <div class="reply">
# 					    </div>
# 				    </div>
# 		        </li><!-- #comment-## -->
# 		        <li class="comment odd alt thread-odd thread-alt depth-1" id="comment-102506">
# 				    <div id="div-comment-102506" class="comment-body">
# 				        <div class="comment-author vcard">
# 			                <img alt='' src='http://1.gravatar.com/avatar/9b8b9b1dfe2bf0e7d5c2038d7d8c1ec1?s=32&amp;d=http%3A%2F%2F1.gravatar.com%2Favatar%2Fad516503a11cd5ca435acc9bb6523536%3Fs%3D32&amp;r=G' class='avatar avatar-32 photo' height='32' width='32' />
# 			                <cite class="fn">Simon</cite> 
# 			                <span class="says">says:</span>		
# 			            </div>
# 		                <div class="comment-meta commentmetadata">
# 		                    <a href="http://www.myex.com/ex/aide-badilla/#comment-102506">
# 			July 20, 2014 at 4:20 am</a>		
# 			            </div>
# 		                <p>More than happy to test your theories out, she&#8217;s do-able.</p>
#                         <div class="reply">
# 				        </div>
# 				    </div>
# 		        </li><!-- #comment-## -->
# 	        </ol>