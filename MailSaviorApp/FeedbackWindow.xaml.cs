using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;

namespace MailSaviorApp
{
    public partial class FeedbackWindow : Window
    {
        public FeedbackWindow()
        {
            InitializeComponent();
            LoadFeedbacks();
        }

        private async void LoadFeedbacks()
        {
            string apiUrl = "http://127.0.0.1:8000/feedbacks";

            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.GetAsync(apiUrl);
                    response.EnsureSuccessStatusCode();

                    string result = await response.Content.ReadAsStringAsync();
                    var feedbacks = JsonSerializer.Deserialize<List<FeedbackEntry>>(result);
                    FeedbackListView.ItemsSource = feedbacks;
                }
                catch (HttpRequestException ex)
                {
                    MessageBox.Show($"Erreur lors du chargement : {ex.Message}");
                }
            }
        }
    }

    public class FeedbackEntry
    {
        public string text { get; set; }
        public double score { get; set; }
        public string feedback { get; set; }
    }
}
