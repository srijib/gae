using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Crawler.Common;
using Crawler.Database;
using Crawler.Database.Table;

namespace Crawler.Model
{
    class Crawler : IDisposable
    {
        private const int MaxWorkerCount = 5;

        private const string PageLinkRegEx = "<a.*?href\\s*=\\s*[\'\"\\s]*(.*?)(?:[\'\">]|$)";
        private const string PageTitleRegEx = "<title>(.*?)</title>";
        private const string ImageLinkRegEx = "http://..img.\\.mnsfz\\.com/big/.+?\\.jpg";
        private const int DelayTimeMilliseconds = 1000;

        private volatile bool isRunning = true;
        private string domainUri;
        private DBManager db = new DBManager();

        public Crawler(string domainUri)
        {
            this.domainUri = domainUri;
        }

        public void NotifyWorkersStop()
        {
            this.isRunning = false;
        }

        public async Task StartOrContinue()
        {
            await this.db.CreateTablesAsync();
            Link link = await this.db.GetNextPendingLinkAsync();
            if (link == null)
            {
                var initLink = new Link { Uri = this.domainUri, Type = LinkType.Page, Status = LinkStatus.Pending };
                await this.db.EnqueueLinksEnsureUniqueAsync(new List<Link> { initLink });
            }

            this.isRunning = true;
            for (int i = 0; i < MaxWorkerCount; i++)
            {
                await Task.Factory.StartNew(this.ThreadWorker);
            }
        }

        private async void ThreadWorker()
        {
            while (this.isRunning)
            {
                Link nextLink = await this.db.GetNextPendingLinkAsync();
                if (nextLink == null)
                {
                    await Task.Delay(DelayTimeMilliseconds);
                    await Utils.LogAsync("nextLink is null, wait for a moment.");
                }
                else
                {
                    string link = nextLink.Uri;
                    if (IsPageLink(link))
                    {
                        await this.HandlePageLinkAsync(link);
                    }
                    else if (IsImageLink(link))
                    {
                        await this.HandleImageLinkAsync(link);
                    }
                }
            }

            await Utils.LogAsync(string.Format("Thread {0} exited", Thread.CurrentThread.ManagedThreadId));
        }

        private async Task HandleImageLinkAsync(string imageLink)
        {
            await this.DownloadAndSaveImageAsync(imageLink);
        }

        private async Task HandlePageLinkAsync(string pageLink)
        {
            string content = await this.DownloadAndSavePageAsync(pageLink);
            if (content == null) return;


            List<string> pageLinks = this.ParsePageLinks(pageLink, content);
            List<string> imageLinks = ParseImageLinks(pageLink, content);

            await this.db.EnqueueLinksEnsureUniqueAsync(from link in imageLinks select new Link { Uri = link, Type = LinkType.Image, Status = LinkStatus.Pending });
            await this.db.EnqueueLinksEnsureUniqueAsync(from link in pageLinks select new Link { Uri = link, Type = LinkType.Page, Status = LinkStatus.Pending });

            await Utils.LogAsync(string.Format("Page : {0} saved. It has {1} page links, {2} image links.", pageLink, pageLinks.Count, imageLinks.Count));
        }

        private static string ParsePageTitle(string content)
        {
            var match = Regex.Match(content, PageTitleRegEx);
            if (match.Groups.Count == 2)
            {
                return match.Groups[1].Value;
            }
            else
            {
                return string.Empty;
            }
        }

        public void Dispose()
        {
        }

        /*
        public async Task<bool> ProcessNextPageAsync()
        {
            HtmlPage page = await this.db.FirstAsync<HtmlPage>();
            if (page == null)
            {
                Console.WriteLine("Page is null, exit!");
                return false;
            }

            List<string> pageLinks = this.ParsePageLinks(page.Uri, page.Content);
            List<string> imageLinks = this.ParseImageLinks(page.Uri, page.Content);

            foreach (string link in pageLinks)
            {
                bool result = ThreadPool.QueueUserWorkItem(this.ProcessPageLink, link);
                if (!result)
                {
                    Console.WriteLine("Error adding page task into ThreadPool.");
                }
            }

            foreach (string link in imageLinks)
            {
                bool result = ThreadPool.QueueUserWorkItem(this.ProcessImageLink, link);
                if (!result)
                {
                    Console.WriteLine("Error adding image task into ThreadPool.");
                }
            }

            return true;
        }*/

        private static string GetAbsoluteUri(string baseUri, string linkUri)
        {
            Uri uri = new Uri(new Uri(baseUri), linkUri);
            return uri.AbsoluteUri;
        }

        //private async void ProcessPageLink(object link)
        //{
        //    string strlink = link as string;
        //    if (strlink == null) return;
        //    if (IsPageLink(strlink))
        //    {
        //        await this.DownloadAndSavePageAsync(strlink);
        //    }
        //}
        //private async void ProcessImageLink(object link)
        //{
        //    string strlink = link as string;
        //    if (strlink == null) return;
        //    if (IsImageLink(strlink))
        //    {
        //        await this.DownloadAndSaveImageAsync(strlink);
        //    }
        //}

        private static bool IsPageLink(string strlink)
        {
            string link = strlink.ToUpperInvariant();
            return link.EndsWith(".HTML", StringComparison.Ordinal) || link.EndsWith("/", StringComparison.Ordinal);
        }

        private async Task<string> DownloadAndSavePageAsync(string pageLink)
        {
            WebClient client = new WebClient();
            byte[] data;
            try
            {
                data = await client.DownloadDataTaskAsync(pageLink);
            }
            catch (WebException e)
            {
                Utils.LogSync(e.Message);
                return null;
            }

            HtmlPage page = new HtmlPage();
            page.Uri = pageLink;
            page.Content = data;
            string content = Encoding.UTF8.GetString(data);
            Post postInfo = ParsePostInfoByPageContent(content);

            if (postInfo != null)
            {
                await this.db.InsertOrUpdatePostAsync(postInfo);
                page.PostId = postInfo.Id;
            }
            else
            {
                Utils.LogSync("Page: " + page.Uri + " have not a valid title format, can't parse post info.");
            }

            await this.db.InsertOrUpdatePageAsync(page);
            await Utils.LogAsync(string.Format("downloaded and saved page link into database: {0}", pageLink));
            client.Dispose();
            return content;
        }

        /// <summary>
        /// Parses the content of the post info by page.
        /// </summary>
        /// <param name="content">The content.</param>
        /// <returns></returns>
        private static Post ParsePostInfoByPageContent(string content)
        {
            string pageTitle = ParsePageTitle(content);
            // try split and use it to store into db
            if (pageTitle == null)
            {
                pageTitle = string.Empty;
            }

            var parts = pageTitle.Split('-');
            if (parts.Count() == 3)
            {
                Post postInfo = new Post { Category = parts[1], Title = parts[0] };
                return postInfo;
            }
            else
            {
                return null;
            }
        }

        private async Task DownloadAndSaveImageAsync(string imageLink)
        {
            // todo check exist link page then download
            WebClient client = new WebClient();
            byte[] data;
            try
            {
                data = await client.DownloadDataTaskAsync(imageLink);
            }
            catch (WebException e)
            {
                Utils.LogSync(e.Message);
                return;
            }

            string path = GetImagePath(imageLink);
            await FileIO.WriteFileAsync(path, data);
            Image image = new Image();
            image.Uri = imageLink;
            image.LocalPath = path;
            await this.db.InsertAsync(image);
            await Utils.LogAsync(string.Format("downloaded image link: {0} and saved to local: {1}", imageLink, path));
            client.Dispose();
        }

        private static string GetImagePath(string strlink)
        {
            Uri uri = new Uri(strlink);
            return string.Join(string.Empty, uri.Segments.Skip(1));
        }

        public static bool IsImageLink(string link)
        {
            string lowerLink = link.ToUpperInvariant();
            return lowerLink.EndsWith(".JPG", StringComparison.Ordinal) || lowerLink.EndsWith(".PNG", StringComparison.Ordinal);
        }

        private List<string> ParsePageLinks(string baseUri, string content)
        {
            List<string> links = new List<string>();
            MatchCollection linkMatches = Regex.Matches(content, PageLinkRegEx);
            foreach (Match item in linkMatches)
            {
                if (item.Groups != null && item.Groups.Count >= 2)
                {
                    string link = item.Groups[1].Value;
                    if (link != "#" && !link.Contains("javascript:void(0)"))
                    {
                        if (!(link.StartsWith("http", StringComparison.Ordinal) && !link.Contains(this.domainUri)))
                        {
                            links.Add(GetAbsoluteUri(baseUri, link));
                        }
                    }
                }
            }
            return links;
        }

        private static List<string> ParseImageLinks(string baseUri, string content)
        {
            List<string> links = new List<string>();
            MatchCollection imageMatches = Regex.Matches(content, ImageLinkRegEx);
            foreach (Match item in imageMatches)
            {
                if (item.Groups != null && item.Groups.Count >= 1)
                {
                    string link = item.Groups[0].Value;
                    if (link != "#" && !link.Contains("javascript:void(0)"))
                    {
                        link = link.Replace("big", "pic");
                        links.Add(GetAbsoluteUri(baseUri, link));
                    }
                }
            }
            return links;
        }
    }
}
