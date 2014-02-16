using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Crawler.Database.Table;
using SQLite;

namespace Crawler.Database
{
    class DBManager
    {
        private const string DBPath = "database.db";
        private readonly SQLiteAsyncConnection dbConnection = new SQLiteAsyncConnection(DBPath);

        public DBManager()
        {
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Performance", "CA1821:RemoveEmptyFinalizers")]
        ~DBManager()
        {
        }

        public async Task CreateTablesAsync()
        {
            await this.dbConnection.CreateTablesAsync<Link, HtmlPage, Image, Post>();
        }

        public async Task EnqueueLinksEnsureUniqueAsync(IEnumerable<Link> links)
        {
            await this.dbConnection.RunInTransactionAsync(conn =>
            {
                foreach (Link link in links)
                {
                    Link exitedLink = conn.Table<Link>().Where(m => m.Uri == link.Uri).FirstOrDefault();
                    if (exitedLink == null)
                    {
                        conn.Insert(link);
                    }
                }
            });
        }

        public async Task<Link> GetNextPendingLinkAsync()
        {
            Link link = null;
            await this.dbConnection.RunInTransactionAsync(conn =>
            {
                link = conn.Table<Link>().Where(m => m.Status == LinkStatus.Pending && m.Type == LinkType.Image).FirstOrDefault();
                if (link == null)
                {
                    link = conn.Table<Link>().Where(m => m.Status == LinkStatus.Pending).FirstOrDefault();
                }
                if (link != null)
                {
                    link.Status = LinkStatus.Processing;
                    conn.Update(link);
                }
            });

            return link;
        }

        public async Task InsertAsync(TableBase item)
        {
            await this.dbConnection.InsertAsync(item);
        }

        public async Task InsertOrUpdatePageAsync(HtmlPage page)
        {
            await this.dbConnection.RunInTransactionAsync(conn =>
            {
                HtmlPage existItem = conn.Table<HtmlPage>().Where(m => m.Uri == page.Uri).FirstOrDefault();
                if (existItem == null)
                {
                    conn.Insert(page);
                }
                else
                {
                    conn.Update(page);
                }
            });
        }

        /// <summary>
        /// Inserts the or update post async.
        /// </summary>
        /// <param name="post">The post.</param>
        /// <returns>The task.</returns>
        public async Task InsertOrUpdatePostAsync(Post post)
        {
            await this.dbConnection.RunInTransactionAsync(conn =>
            {
                Post existItem = conn.Table<Post>().Where(m => m.Category == post.Category && m.Title == post.Title).FirstOrDefault();
                if (existItem == null)
                {
                    conn.Insert(post);
                }
                else
                {
                    conn.Update(post);
                }
            });
        }

        //public async Task<T> FirstAsync<T>() where T : TableBase, new()
        //{
        //    var item = await this.dbConnection.Table<T>().OrderBy(m => m.Id).FirstOrDefaultAsync();
        //    return item;
        //}

        //public async Task<bool> DeleteAsync<T>(T item) where T : TableBase, new()
        //{
        //    int rowsAffected = await this.dbConnection.DeleteAsync(item);
        //    return rowsAffected > 0;
        //}
    }
}
