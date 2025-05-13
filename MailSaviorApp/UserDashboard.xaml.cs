using System.Windows;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace MailSaviorApp
{
    public partial class UserDashboard : Window
    {
        private string lastAnalyzedText = "";
        private double lastAnalyzedScore = 0;

        public UserDashboard()
        {
            InitializeComponent();
        }


        private async void FeedbackYes_Click(object sender, RoutedEventArgs e)
        {
            await SendFeedbackAsync(lastAnalyzedText, lastAnalyzedScore, "phishing");
        }

        private async void FeedbackNo_Click(object sender, RoutedEventArgs e)
        {
            await SendFeedbackAsync(lastAnalyzedText, lastAnalyzedScore, "safe");
        }

        private async void Analyze_Click(object sender, RoutedEventArgs e)
        {
            string emailText = EmailInput.Text;
            string apiUrl = "http://127.0.0.1:8000/analyze_email";

            using (HttpClient client = new HttpClient())
            {
                var data = new { text = emailText };
                var json = JsonSerializer.Serialize(data);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                try
                {
                    HttpResponseMessage response = await client.PostAsync(apiUrl, content);
                    response.EnsureSuccessStatusCode();

                    string result = await response.Content.ReadAsStringAsync();
                    using JsonDocument doc = JsonDocument.Parse(result);
                    double score = doc.RootElement.GetProperty("suspicion_score").GetDouble();

                    // Stocker pour le feedback
                    lastAnalyzedText = emailText;
                    lastAnalyzedScore = score;

                    ScoreResult.Text = $"Score de suspicion : {score * 100:0.0}%";
                    FeedbackPanel.Visibility = Visibility.Visible;
                }
                catch (Exception ex)
                {
                    ScoreResult.Text = $"Erreur lors de l'analyse : {ex.Message}";
                }
            }
        }



        public async Task SendFeedbackAsync(string emailText, double score, string feedback)
        {
            var client = new HttpClient();
            var feedbackData = new AnalysisFeedback
            {
                text = emailText,
                score = score,
                feedback = feedback
            };

            var response = await client.PostAsJsonAsync("http://localhost:8000/feedback", feedbackData);
            if (response.IsSuccessStatusCode)
            {
                MessageBox.Show("Feedback envoye avec succes !");
            }
            else
            {
                MessageBox.Show("Erreur lors de l’envoi du feedback.");
            }
        }

        private void OpenFeedbackWindow_Click(object sender, RoutedEventArgs e)
        {
            FeedbackWindow fw = new FeedbackWindow();
            fw.Show();
        }

    }
}
