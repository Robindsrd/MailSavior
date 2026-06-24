using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Windows;

namespace MailSaviorApp
{
    public partial class FeedbackWindow : Window
    {
        private static readonly HttpClient client = new HttpClient
        {
            BaseAddress = new Uri(ApiConfig.BaseUrl),
            Timeout = ApiConfig.Timeout
        };

        public FeedbackWindow()
        {
            InitializeComponent();
            LoadFeedbacks();
        }

        private async void LoadFeedbacks()
        {
            try
            {
                var feedbacks = await client.GetFromJsonAsync<List<FeedbackEntry>>("/feedbacks");
                FeedbackListView.ItemsSource = feedbacks;
            }
            catch (Exception)
            {
                MessageBox.Show("Impossible de charger les feedbacks (service indisponible).");
            }
        }
    }

    /// <summary>
    /// Reflète le schéma minimisé renvoyé par l'API : pas de corps d'e-mail stocké.
    /// </summary>
    public class FeedbackEntry
    {
        public string created_at { get; set; }
        public string predicted_label { get; set; }
        public double suspicion_score { get; set; }
        public string feedback_label { get; set; }
        public bool feedback_correct { get; set; }
        public int? text_length { get; set; }
    }
}
