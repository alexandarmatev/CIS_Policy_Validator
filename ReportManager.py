from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


class ReportManager:
    def __init__(self, evaluated_recommendations, all_domains_weight):
        self._evaluated_recommendations = list(evaluated_recommendations)
        self._all_domains_weight = all_domains_weight

    def _get_audited_recommendations_details(self):
        audited_recommendations = []
        compliant_recommendations = []
        for recommendation in self._evaluated_recommendations:
            if recommendation.compliant:
                compliant_recommendations.append(recommendation.cis_control.domain)
            audited_recommendations.append(recommendation.cis_control.domain)
        return Counter(audited_recommendations), Counter(compliant_recommendations)

    def _create_domains_weight_pie_chart(self):
        percentages = self._all_domains_weight

        labels = percentages.keys()
        sizes = percentages.values()

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('All Control Domains Weight')

        plt.savefig('report_images/control_domains_weight_chart.png')

    def _create_compliant_recommendations_bar_chart(self):
        audited_recommendations_count, compliant_recommendations_count = self._get_audited_recommendations_details()

        domains = list(audited_recommendations_count.keys())
        total_values = [audited_recommendations_count[domain] for domain in domains]
        compliant_values = [compliant_recommendations_count[domain] for domain in domains]

        # Setting up the bar positions
        bar_width = 0.3  # Width of the bars
        index = np.arange(len(domains))

        # Creating the bar chart
        fig, ax = plt.subplots()
        bar1 = ax.bar(index, total_values, bar_width, color='cornflowerblue', label='Total Count')
        bar2 = ax.bar(index + bar_width, compliant_values, bar_width, color='lightcoral', label='Compliant Count')

        # Adding labels for the counts centered over the bars
        for i in range(len(domains)):
            # Position for the total counts
            ax.text(i, total_values[i] + max(total_values) * 0.03, str(total_values[i]), ha='center', va='bottom', fontsize=9)

            # Position for the compliant counts
            ax.text(i + bar_width, compliant_values[i] + max(total_values) * 0.03, str(compliant_values[i]), ha='center', va='bottom', fontsize=9)

        # Adjusting the y-axis limit to ensure labels don't go outside the grid
        ax.set_ylim(0, max(total_values) + max(total_values) * 0.1)

        # Adding labels, title, and legend
        ax.set_xlabel('Domain')
        ax.set_ylabel('Counts')
        ax.set_title('Comparison of Total and Compliant Recommendations by Domain')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(domains)
        ax.legend()

        plt.savefig('report_images/compliance_bar_chart.png', bbox_inches='tight')