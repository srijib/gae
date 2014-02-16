using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLite;

namespace Crawler.Database.Table
{
    class Post : TableBase
    {
        [MaxLength(256), Indexed]
        public string Title { get; set; }
        [MaxLength(256), Indexed]
        public string Category { get; set; }
    }
}
