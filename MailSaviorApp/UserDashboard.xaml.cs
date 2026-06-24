using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;

namespace MailSaviorApp
{
    public partial class UserDashboard : Window
    {
        // HttpClient réutilisé (pas de recréation à chaque clic) + timeout configuré.
        private static readonly HttpClient client = new HttpClient
        {
            BaseAddress = new Uri(ApiConfig.BaseUrl),
            Timeout = ApiConfig.Timeout
        };

        private string lastPredictedLabel = "";
        private double lastScore = 0;
        private int lastTextLength = 0;

        public UserDashboard()
        {
            InitializeComponent();
        }

        private async void Analyze_Click(object sender, RoutedEventArgs e)
        {
            string emailText = EmailInput.Text;
            if (string.IsNullOrWhiteSpace(emailText))
            {
                ShowMessage("Veuillez saisir le texte d'un e-mail.", Brushes.Black);
                return;
            }

            SetLoading(true);
            FeedbackPanel.Visibility = Visibility.Collapsed;
            try
            {
                var response = await client.PostAsJsonAsync("/analyze_email", new { text = emailText });
                if (!response.IsSuccessStatusCode)
                {
                    ShowMessage("Le service d'analyse est momentanément indisponible.", Brushes.Black);
                    return;
                }

                var result = await response.Content.ReadFromJsonAsync<AnalyzeResult>();
                lastPredictedLabel = result.label;
                lastScore = result.suspicion_score;
                lastTextLength = emailText.Length;

                // Accessibilité : le verdict est explicite en texte, pas seulement via la couleur.
                string verdict = result.label == "phishing" ? "⚠ PHISHING détecté" : "✓ Message sûr";
                ShowMessage(
                    $"{verdict}   |   Score de suspicion : {result.suspicion_score * 100:0.0}%   |   Modèle v{result.model_version}",
                    result.label == "phishing" ? Brushes.DarkRed : Brushes.DarkGreen);
                FeedbackPanel.Visibility = Visibility.Visible;
            }
            catch (TaskCanceledException)
            {
                ShowMessage("Délai dépassé : le service d'analyse ne répond pas.", Brushes.Black);
            }
            catch (HttpRequestException)
            {
                ShowMessage("Connexion impossible au service d'analyse.", Brushes.Black);
            }
            finally
            {
                SetLoading(false);
            }
        }

        private async void FeedbackYes_Click(object sender, RoutedEventArgs e)
            => await SendFeedbackAsync("phishing");

        private async void FeedbackNo_Click(object sender, RoutedEventArgs e)
            => await SendFeedbackAsync("safe");

        private async Task SendFeedbackAsync(string feedback)
        {
            try
            {
                var payload = new AnalysisFeedback
                {
                    suspicion_score = lastScore,
                    feedback = feedback,
                    predicted_label = lastPredictedLabel,
                    text_length = lastTextLength
                };
                var response = await client.PostAsJsonAsync("/feedback", payload);
                MessageBox.Show(response.IsSuccessStatusCode
                    ? "Feedback envoyé avec succès !"
                    : "Erreur lors de l'envoi du feedback.");
            }
            catch (Exception)
            {
                MessageBox.Show("Connexion impossible : feedback non envoyé.");
            }
        }

        private void OpenFeedbackWindow_Click(object sender, RoutedEventArgs e)
        {
            FeedbackWindow fw = new FeedbackWindow();
            fw.Show();
        }

        private void ShowMessage(string text, Brush color)
        {
            ScoreResult.Text = text;
            ScoreResult.Foreground = color;
        }

        private void SetLoading(bool loading)
        {
            AnalyzeButton.IsEnabled = !loading;
            AnalyzeButton.Content = loading ? "Analyse en cours..." : "Analyser";
        }

        private class AnalyzeResult
        {
            public string label { get; set; }
            public double suspicion_score { get; set; }
            public string model_version { get; set; }
        }
    }
}
