from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from database import Database
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = Database(app.config['DATABASE_PATH'])

@app.route('/')
def home():
    """Homepage"""
    testimonials = db.get_testimonials(featured_only=True)
    blog_posts = db.get_blog_posts(limit=3)
    return render_template('home.html', 
                         testimonials=testimonials,
                         blog_posts=blog_posts)

@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html')

@app.route('/ai-products')
def ai_products():
    """AI Products page"""
    return render_template('ai-products.html')

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@app.route('/blog')
def blog():
    """Blog listing page"""
    category = request.args.get('category')
    blog_posts = db.get_blog_posts(category=category)
    categories = ['Technical SEO', 'Content Marketing', 'AI Tools', 'Case Studies', 'Industry News']
    return render_template('blog.html', 
                         blog_posts=blog_posts, 
                         categories=categories,
                         current_category=category)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post"""
    post = db.get_blog_post_by_slug(slug)
    if not post:
        return "Blog post not found", 404
    
    # Get related posts from same category
    related_posts = db.get_blog_posts(limit=3, category=post['category'])
    
    return render_template('blog-post.html', 
                         post=post, 
                         related_posts=related_posts)

@app.route('/case-studies')
def case_studies():
    """Case studies listing"""
    return render_template('case-studies.html')

@app.route('/case-studies/<slug>')
def case_study(slug):
    """Individual case study"""
    # In a real app, you'd fetch this from database
    return render_template('case-study.html', slug=slug)

@app.route('/resources')
def resources():
    """Resources page"""
    return render_template('resources.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'company': request.form.get('company'),
            'website': request.form.get('website'),
            'service_interested': request.form.get('service_interested'),
            'monthly_traffic': request.form.get('monthly_traffic'),
            'budget_range': request.form.get('budget_range'),
            'referral_source': request.form.get('referral_source'),
            'message': request.form.get('message')
        }
        
        try:
            contact_id = db.insert_contact(data)
            flash('Thank you for contacting us! We\'ll get back to you within 24 hours.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('contact.html')

@app.route('/faq')
def faq():
    """FAQ page"""
    faqs = {
        'General SEO Questions': [
            {
                'question': 'What is SEO and why do I need it?',
                'answer': 'SEO (Search Engine Optimization) is the practice of optimizing your website to rank higher in search engine results. You need it because 93% of online experiences begin with a search engine, and 75% of users never scroll past the first page of results. SEO helps you attract organic (free) traffic, build credibility, and increase conversions.'
            },
            {
                'question': 'How long does SEO take to show results?',
                'answer': 'SEO is a long-term strategy. Typically, you\'ll start seeing initial improvements in 3-6 months, with significant results appearing around 6-12 months. However, the timeline varies based on your industry competition, current website status, and the scope of optimization work required.'
            },
            {
                'question': 'What\'s the difference between on-page and off-page SEO?',
                'answer': 'On-page SEO refers to optimizations made directly on your website (content, meta tags, site structure, speed). Off-page SEO includes activities outside your website that impact rankings, primarily link building, social signals, and brand mentions.'
            },
            {
                'question': 'Do I need to keep paying for SEO every month?',
                'answer': 'SEO requires ongoing maintenance because search algorithms constantly evolve, competitors are always optimizing, and fresh content signals relevance to search engines. However, the work you\'ve done doesn\'t disappear—it compounds over time, making each month more effective than the last.'
            },
            {
                'question': 'Can you guarantee #1 rankings on Google?',
                'answer': 'No reputable SEO agency can guarantee #1 rankings, as Google\'s algorithm has over 200 ranking factors and is constantly changing. We focus on sustainable, white-hat strategies that improve your overall visibility and deliver measurable traffic and conversion increases.'
            }
        ],
        'Our Services': [
            {
                'question': 'What\'s included in your SEO packages?',
                'answer': 'Our packages include keyword research, on-page optimization, technical SEO audits, content creation, link building, monthly reporting, and access to our AI-powered SEO tools. The specific scope varies by plan—check our pricing page for detailed comparisons.'
            },
            {
                'question': 'Do you offer custom packages?',
                'answer': 'Yes! While we have standard packages for most businesses, we understand every company has unique needs. Contact us for a custom quote tailored to your specific goals, industry, and budget.'
            },
            {
                'question': 'Can I cancel anytime?',
                'answer': 'Yes, all our plans are month-to-month with no long-term contracts required. We earn your business every month by delivering results. However, we recommend committing to at least 6 months to see the full impact of SEO efforts.'
            },
            {
                'question': 'Will I have a dedicated account manager?',
                'answer': 'Growth and Enterprise plans include dedicated account managers. Starter plan clients work with our support team and can upgrade anytime for more personalized service.'
            },
            {
                'question': 'Do you work with businesses in my industry?',
                'answer': 'We work with clients across e-commerce, SaaS, healthcare, legal, real estate, finance, and many other industries. Our AI-powered approach adapts to any niche, and we\'ve delivered results in competitive markets.'
            }
        ],
        'AI Products': [
            {
                'question': 'How does AI improve SEO?',
                'answer': 'Our AI tools analyze millions of data points to identify high-value keywords, predict content performance, detect technical issues faster, and provide insights that would take humans weeks to uncover manually. AI also helps us scale personalized strategies across hundreds of pages efficiently.'
            },
            {
                'question': 'Are your AI tools included in all plans?',
                'answer': 'Basic access to our AI tools is included in Growth and Enterprise plans. Starter plan clients can add AI tools for an additional fee. We also offer standalone subscriptions for businesses managing SEO in-house.'
            },
            {
                'question': 'Can I use AI tools separately without full SEO services?',
                'answer': 'Yes! Our AI Keyword Explorer, Content Optimizer, Rank Tracker Pro, and Technical SEO Auditor are available as standalone products. Visit our AI Products page for pricing details.'
            },
            {
                'question': 'Is the content generated by AI unique and safe to use?',
                'answer': 'Our AI Content Generator creates original, plagiarism-free content that passes all duplicate content checks. However, we always recommend human review and editing to ensure brand voice alignment and factual accuracy. AI is a tool to enhance efficiency, not replace human expertise.'
            },
            {
                'question': 'Will Google penalize AI-generated content?',
                'answer': 'Google doesn\'t penalize content simply for being AI-generated. Their focus is on content quality, helpfulness, and user experience. Our AI tools help create high-quality, user-focused content that aligns with Google\'s E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) guidelines.'
            }
        ],
        'Pricing & Contracts': [
            {
                'question': 'Are there any setup fees?',
                'answer': 'No, we don\'t charge setup fees. You pay only the monthly package rate, and we get started immediately after onboarding.'
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept all major credit cards (Visa, Mastercard, Amex, Discover), ACH bank transfers, and PayPal. Enterprise clients can also arrange for invoicing with NET-30 payment terms.'
            },
            {
                'question': 'Do you require long-term contracts?',
                'answer': 'No, all our plans are month-to-month. While we recommend a 6-12 month commitment for optimal results, you\'re free to cancel anytime without penalties.'
            },
            {
                'question': 'What happens if I\'m not satisfied?',
                'answer': 'We offer a 30-day money-back guarantee. If you\'re not satisfied with our service in the first month, we\'ll refund your payment, no questions asked.'
            },
            {
                'question': 'Can I upgrade or downgrade my plan?',
                'answer': 'Absolutely! You can change your plan anytime. Upgrades take effect immediately, while downgrades take effect at your next billing cycle.'
            }
        ]
    }
    return render_template('faq.html', faqs=faqs)

@app.route('/free-audit', methods=['GET', 'POST'])
def free_audit():
    """Free SEO audit request page"""
    if request.method == 'POST':
        data = {
            'website_url': request.form.get('website_url'),
            'email': request.form.get('email'),
            'industry': request.form.get('industry'),
            'competitor1': request.form.get('competitor1'),
            'competitor2': request.form.get('competitor2'),
            'competitor3': request.form.get('competitor3')
        }
        
        try:
            audit_id = db.insert_audit_request(data)
            flash('Your free SEO audit request has been received! Check your email for the report within 24 hours.', 'success')
            return redirect(url_for('free_audit'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('free-audit.html')

@app.route('/careers')
def careers():
    """Careers page"""
    jobs = [
        {
            'title': 'Senior SEO Specialist',
            'location': 'Remote',
            'type': 'Full-time',
            'department': 'SEO',
            'description': 'Lead SEO strategies for enterprise clients and mentor junior team members.'
        },
        {
            'title': 'Content Writer (SEO Focus)',
            'location': 'San Francisco, CA / Remote',
            'type': 'Full-time',
            'department': 'Content',
            'description': 'Create high-quality, SEO-optimized content for clients across industries.'
        },
        {
            'title': 'AI/ML Engineer',
            'location': 'San Francisco, CA',
            'type': 'Full-time',
            'department': 'Engineering',
            'description': 'Develop and enhance our AI-powered SEO tools and algorithms.'
        }
    ]
    return render_template('careers.html', jobs=jobs)

@app.route('/terms')
def terms():
    """Terms of Service page"""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

# API Routes
@app.route('/api/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Newsletter subscription API"""
    email = request.form.get('email') or request.json.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    success = db.subscribe_newsletter(email)
    
    if success:
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    else:
        return jsonify({'success': False, 'message': 'Email already subscribed'}), 400

@app.route('/api/download/<resource>', methods=['POST'])
def download_resource(resource):
    """Resource download with email capture"""
    email = request.form.get('email') or request.json.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    # Log download
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resource_downloads (resource_name, user_email)
        VALUES (?, ?)
    ''', (resource, email))
    conn.commit()
    conn.close()
    
    # In production, you'd send an email with the download link
    return jsonify({
        'success': True, 
        'message': 'Check your email for the download link!',
        'download_url': f'/static/resources/{resource}.pdf'
    })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# Template filters
@app.template_filter('format_date')
def format_date(date_string):
    """Format date for display"""
    if isinstance(date_string, str):
        try:
            dt = datetime.fromisoformat(date_string)
            return dt.strftime('%B %d, %Y')
        except:
            return date_string
    return date_string

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
