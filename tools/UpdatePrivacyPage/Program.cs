using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Nodes;

var repoRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));
var i18nDir = Path.Combine(repoRoot, "i18n");
var jaPrivacy = JsonNode.Parse(File.ReadAllText(Path.Combine(repoRoot, "tools", "privacy-sections-ja.json")))!;
var enPrivacy = JsonNode.Parse(File.ReadAllText(Path.Combine(repoRoot, "tools", "privacy-sections-en.json")))!;

var writeOptions = new JsonSerializerOptions
{
    WriteIndented = true,
    Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
};

foreach (var file in Directory.GetFiles(i18nDir, "*.json"))
{
    var lang = Path.GetFileNameWithoutExtension(file);
    var root = JsonNode.Parse(File.ReadAllText(file))!.AsObject();
    var privacy = (lang == "ja" ? jaPrivacy : enPrivacy).DeepClone();
    if (root["privacyPage"] is JsonObject existing &&
        existing["metaTitle"] is JsonValue metaTitle &&
        lang != "ja" &&
        lang != "en")
    {
        privacy["metaTitle"] = metaTitle.DeepClone();
        privacy["title"] = existing["title"]?.DeepClone() ?? privacy["title"]!.DeepClone();
        privacy["updated"] = existing["updated"]?.DeepClone() ?? privacy["updated"]!.DeepClone();
    }

    root["privacyPage"] = privacy;
    File.WriteAllText(file, JsonSerializer.Serialize(root, writeOptions) + Environment.NewLine);
    Console.WriteLine($"Updated {Path.GetFileName(file)}");
}
