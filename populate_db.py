#!/usr/bin/env python3
"""
Sample data population script for SEOversion database
Run this after starting the app for the first time
"""

from database import Database

db = Database('seoversion.db')
conn = db.get_connection()
cursor = conn.cursor()

print("Populating database with sample data...")

# Sample Blog Posts
blog_posts = [
    {
        'title': 'Top 10 SEO Trends for 2026',
        'slug': 'top-10-seo-trends-2026',
        'content': '''The SEO landscape is constantly evolving. Here are the top 10 trends that will dominate 2026:

1. AI-Generated Content Optimization
Search engines are getting better at understanding AI-generated content. The key is ensuring it provides genuine value and expertise.

2. Voice Search Optimization
With smart speakers in millions of homes, optimizing for conversational queries is more important than ever.

3. Video SEO
Video content is dominating search results. YouTube optimization and video schema markup are critical.

4. Core Web Vitals
Page experience signals continue to be ranking factors. Speed, interactivity, and visual stability matter more than ever.

5. E-A-T (Expertise, Authoritativeness, Trustworthiness)
Google increasingly favors content from recognized experts and authoritative sources.

[Continue with remaining trends...]''',
        'excerpt': 'Discover the latest SEO trends that will dominate 2026 and how to adapt your strategy for maximum visibility.',
        'category': 'Industry News'
    },
    {
        'title': 'How AI is Revolutionizing Keyword Research',
        'slug': 'ai-revolutionizing-keyword-research',
        'content': '''Traditional keyword research is time-consuming and often misses hidden opportunities. AI is changing the game...''',
        'excerpt': 'Learn how artificial intelligence is transforming keyword research and helping marketers discover untapped opportunities.',
        'category': 'AI Tools'
    },
    {
        'title': 'Complete Technical SEO Checklist for 2026',
        'slug': 'technical-seo-checklist-2026',
        'content': '''Technical SEO forms the foundation of your website's search performance. Use this comprehensive checklist...''',
        'excerpt': 'A step-by-step technical SEO checklist to ensure your website is optimized for search engines and users.',
        'category': 'Technical SEO'
    }
]

for post in blog_posts:
    try:
        cursor.execute('''
            INSERT INTO blog_posts (title, slug, content, excerpt, category, views)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post['title'], post['slug'], post['content'], post['excerpt'], post['category'], 0))
        print(f"✓ Added blog post: {post['title']}")
    except Exception as e:
        print(f"✗ Error adding blog post: {e}")

# Sample Testimonials
testimonials = [
    {
        'client_name': 'Sarah Johnson',
        'company': 'TechStart Solutions',
        'rating': 5,
        'testimonial_text': 'SEOversion transformed our online presence completely. Within 6 months, our organic traffic increased by 300% and we\'re now ranking #1 for our most valuable keywords. The AI-powered insights were game-changing.',
        'featured': 1
    },
    {
        'client_name': 'Michael Chen',
        'company': 'GreenLeaf Wellness',
        'rating': 5,
        'testimonial_text': 'Best SEO agency we\'ve worked with. The team is responsive, transparent, and most importantly, they deliver results. Our lead generation has increased 5x since starting with SEOversion.',
        'featured': 1
    },
    {
        'client_name': 'Emily Rodriguez',
        'company': 'Urban Real Estate Group',
        'rating': 5,
        'testimonial_text': 'The ROI has been incredible. We were skeptical about SEO at first, but SEOversion proved us wrong. Our website now generates more leads than paid advertising, and the cost per lead is 70% lower.',
        'featured': 1
    }
]

for testimonial in testimonials:
    try:
        cursor.execute('''
            INSERT INTO testimonials (client_name, company, rating, testimonial_text, featured)
            VALUES (?, ?, ?, ?, ?)
        ''', (testimonial['client_name'], testimonial['company'], testimonial['rating'], 
              testimonial['testimonial_text'], testimonial['featured']))
        print(f"✓ Added testimonial from: {testimonial['client_name']}")
    except Exception as e:
        print(f"✗ Error adding testimonial: {e}")

conn.commit()
conn.close()

print("\n✓ Sample data population complete!")
print("\nNext steps:")
print("1. Run 'python app.py' to start the application")
print("2. Visit http://localhost:5000 to see your website")
print("3. Complete the remaining template pages (see README.md)")
