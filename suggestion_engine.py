import pandas as pd
from datetime import datetime, timedelta

def generate_suggestions(expenses):
    df = pd.DataFrame(expenses)
    if df.empty:
        return {
            "categorySuggestions": {},
            "accountSuggestions": [{
                "status": ["⚠️ No Data"],
                "message": "No expense data found. Add expenses to get suggestions.",
                "color": "gray",
                "labelTypes": ["neutral"]
            }]
        }

    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    last_30_days = df[df['date'] >= (datetime.now() - timedelta(days=30))]

    if last_30_days.empty:
        return {
            "categorySuggestions": {},
            "accountSuggestions": [{
                "status": ["🕒 No Recent Activity"],
                "message": "No expenses in the last 30 days. Keep tracking regularly!",
                "color": "gray",
                "labelTypes": ["info"]
            }]
        }

    category_summary = last_30_days.groupby('category')['amount'].sum()
    total_spending = last_30_days['amount'].sum()
    avg_spending = category_summary.mean()

    category_suggestions = {}
    account_suggestions = []

    def get_labels(amount, avg):
        ratio = (amount / avg) * 100 if avg else 0
        labels = []
        color = "gray"

        if ratio < 30:
            labels.append("🧊 Very Low")
            color = "blue"
        elif ratio < 50:
            labels.append("📉 Low")
            color = "lightblue"
        elif ratio < 60:
            labels.append("🙂 Balanced")
            color = "green"
        elif ratio < 80:
            labels.append("🟡 Moderate")
            color = "yellow"
        elif ratio <= 100:
            labels.append("🟢 Normal")
            color = "green"
        elif ratio <= 120:
            labels.append("🟠 Slightly High")
            color = "orange"
        elif ratio <= 150:
            labels.append("🔴 Overbudget")
            color = "red"
        else:
            labels.append("❌ Critical Overspending")
            color = "darkred"

        return labels, color

    def get_label_types(labels):
        types = set()
        for l in labels:
            if "Critical" in l or "Overbudget" in l:
                types.add("danger")
            elif "Slightly High" in l or "Spike" in l:
                types.add("warning")
            elif "Normal" in l:
                types.add("success")
            elif "Balanced" in l:
                types.add("info")
            elif "Low" in l or "Very Low" in l:
                types.add("neutral")
        return list(types) or ["info"]

    def generate_message(category, labels):
        base = f"Category: **{category.capitalize()}** → "
        if any("Critical" in label for label in labels):
            return base + "❌ Spending is extremely high. Cut back urgently!"
        if any("Overbudget" in label for label in labels):
            return base + "⚠️ You're over your usual spending. Try reducing it by 15-20%."
        if any("Slightly High" in label for label in labels):
            return base + "🟠 Slightly above average. Keep monitoring it."
        if any("Normal" in label for label in labels):
            return base + "✅ Spending is within your expected range. Good job!"
        if any("Balanced" in label for label in labels):
            return base + "🙂 Balanced spending. You're doing well!"
        if any("Low" in label for label in labels):
            return base + "📉 Spending is low. Are you missing essentials?"
        if any("Very Low" in label for label in labels):
            return base + "🧊 Very low spending. Make sure you're not under-spending on necessities."
        return base + "No specific advice."

    for category, amount in category_summary.items():
        labels, color = get_labels(amount, avg_spending)
        category_suggestions[category] = {
            "spent": round(float(amount), 2),
            "status": labels,
            "color": color,
            "labelTypes": get_label_types(labels),
            "message": generate_message(category, labels)
        }

    # Account-wide suggestion
    overall_avg = avg_spending * len(category_summary)
    labels, color = get_labels(total_spending, overall_avg)
    account_suggestions.append({
        "totalSpent": round(float(total_spending), 2),
        "status": labels,
        "color": color,
        "labelTypes": get_label_types(labels),
        "message": generate_message("overall account", labels)
    })

    # Anomaly warning
    daily_spend = last_30_days.groupby(last_30_days['date'].dt.date)['amount'].sum()
    if not daily_spend.empty and float(daily_spend.max()) > 1.5 * float(daily_spend.mean()):
        account_suggestions.append({
            "status": ["📈 Daily Spike"],
            "message": "You had spending spikes on certain days. Consider distributing expenses evenly.",
            "color": "orange",
            "labelTypes": ["warning", "spike"]
        })

    return {
        "categorySuggestions": category_suggestions,
        "accountSuggestions": account_suggestions
    }