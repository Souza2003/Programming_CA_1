// QUESTION 2 (PART 1) (C#)

using System;
using System.Collections.Generic;
using System.Linq;

class FileExtensionInfo
{
    public string Extension { get; set; }
    public string FileType { get; set; }
    public string Description { get; set; }
    public string UsedFor { get; set; }

    public FileExtensionInfo(string ext, string type, string desc, string usage)
    {
        Extension = ext;
        FileType = type;
        Description = desc;
        UsedFor = usage;
    }

    public void DisplayInfo()
    {
        Console.WriteLine("\n--- Extension: " + Extension + " ---");
        Console.WriteLine("File Type: " + FileType);
        Console.WriteLine("Description: " + Description);
        Console.WriteLine("Used For: " + UsedFor);
    }
}

class FileExtensionSystem
{
    private Dictionary<string, FileExtensionInfo> extensionDatabase = new Dictionary<string, FileExtensionInfo>();

    public FileExtensionSystem()
    {
        // Video
        AddExt(".mp4", "Video", "MPEG-4 video file", "Streaming videos, YouTube, mobile devices");
        AddExt(".mov", "Video", "Apple QuickTime movie", "Mac video editing, professional video");
        AddExt(".avi", "Video", "Audio Video Interleave", "Windows video files, older format");
        AddExt(".mkv", "Video", "Matroska video file", "High quality video with multiple audio tracks");
        AddExt(".webm", "Video", "WebM video format", "Web videos, HTML5 video streaming");

        // Image
        AddExt(".jpg", "Image", "JPEG image file", "Photos, web images, compressed pictures");
        AddExt(".png", "Image", "Portable Network Graphics", "Web graphics, transparent images, logos");
        AddExt(".gif", "Image", "Graphics Interchange Format", "Animated images, simple graphics");
        AddExt(".bmp", "Image", "Bitmap image file", "Uncompressed images, Windows graphics");
        AddExt(".svg", "Image", "Scalable Vector Graphics", "Web icons, logos, scalable images");

        // Audio
        AddExt(".mp3", "Audio", "MPEG audio layer 3", "Music files, podcasts, audio streaming");
        AddExt(".wav", "Audio", "Waveform audio file", "Uncompressed audio, high quality sound");
        AddExt(".flac", "Audio", "Free Lossless Audio Codec", "High quality music, audiophile recordings");
        AddExt(".aac", "Audio", "Advanced Audio Coding", "iTunes, streaming services, mobile audio");

        // Document
        AddExt(".pdf", "Document", "Portable Document Format", "Documents, ebooks, forms, reports");
        AddExt(".docx", "Document", "Microsoft Word document", "Word processing, letters, reports");
        AddExt(".xlsx", "Document", "Microsoft Excel spreadsheet", "Spreadsheets, data analysis, tables");
        AddExt(".pptx", "Document", "Microsoft PowerPoint presentation", "Presentations, slideshows");

        // Programming/Text
        AddExt(".txt", "Text", "Plain text file", "Simple text, notes, configuration files");
        AddExt(".cs", "Code", "C# source code file", "C# programming, .NET development");
        AddExt(".py", "Code", "Python script file", "Python programming, scripting, automation");
        AddExt(".html", "Web", "HyperText Markup Language", "Web pages, website structure");
        AddExt(".css", "Web", "Cascading Style Sheets", "Web page styling, layout, design");
    }

    private void AddExt(string ext, string type, string desc, string usage)
    {
        extensionDatabase.Add(ext, new FileExtensionInfo(ext, type, desc, usage));
    }

    public void SearchExtension(string query)
    {
        string cleanQuery = query.Trim().ToLower();
        if (!cleanQuery.StartsWith("."))
            cleanQuery = "." + cleanQuery;

        if (extensionDatabase.ContainsKey(cleanQuery))
            extensionDatabase[cleanQuery].DisplayInfo();
        else
        {
            Console.WriteLine("\nSorry, I don't have information about '" + cleanQuery + "' extension.");
            Console.WriteLine("This extension is not in my database.");
            Console.WriteLine("\nWould you like to try another extension?");
        }
    }

    public void ShowAllExtensions()
    {
        Console.WriteLine("\n===== Available File Extensions =====");

        var grouped = extensionDatabase.GroupBy(x => x.Value.FileType);

        foreach (var group in grouped)
        {
            Console.WriteLine("\n" + group.Key + " Files:");
            foreach (var item in group)
                Console.Write(item.Key + "  ");
            Console.WriteLine();
        }
    }

    public int GetExtensionCount()
    {
        return extensionDatabase.Count;
    }
}

class Program
{
    static void Main(string[] args)
    {
        FileExtensionSystem system = new FileExtensionSystem();
        
        Console.WriteLine("===== File Extension Information System =====");
        Console.WriteLine("Database contains " + system.GetExtensionCount() + " file extensions\n");

        bool exit = false;
        while (!exit)
        {
            Console.WriteLine("\n1. Search for file extension");
            Console.WriteLine("2. Show all available extensions");
            Console.WriteLine("3. Exit");
            Console.Write("Choose an option: ");

            switch (Console.ReadLine())
            {
                case "1":
                    Console.Write("\nEnter file extension (e.g., mp4 or .mp4): ");
                    string query = Console.ReadLine();
                    
                    if (string.IsNullOrWhiteSpace(query))
                        Console.WriteLine("Please enter a valid extension.");
                    else
                        system.SearchExtension(query);
                    break;

                case "2":
                    system.ShowAllExtensions();
                    break;

                case "3":
                    exit = true;
                    Console.WriteLine("\nThank you for using the File Extension System!");
                    break;

                default:
                    Console.WriteLine("Invalid option. Please choose 1, 2, or 3.");
                    break;
            }
        }
    }
}
