import sqlite3
from datetime import datetime
import os

class Database:
    """SQLite database handler"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                company TEXT,
                website TEXT,
                service_interested TEXT,
                monthly_traffic TEXT,
                budget_range TEXT,
                referral_source TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'new'
            )
        ''')
        
        # Blog posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                author TEXT DEFAULT 'SEOversion Team',
                category TEXT,
                featured_image TEXT,
                published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                views INTEGER DEFAULT 0,
                status TEXT DEFAULT 'published'
            )
        ''')
        
        # Audit requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_url TEXT NOT NULL,
                email TEXT NOT NULL,
                industry TEXT,
                competitor1 TEXT,
                competitor2 TEXT,
                competitor3 TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                report_sent BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Newsletter subscribers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                subscribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                source TEXT
            )
        ''')
        
        # Resource downloads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Testimonials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS testimonials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                company TEXT,
                rating INTEGER DEFAULT 5,
                testimonial_text TEXT NOT NULL,
                client_photo TEXT,
                featured BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                applicant_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                resume_url TEXT,
                cover_letter TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'new'
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def insert_contact(self, data):
        """Insert contact form submission"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, company, website, 
                                service_interested, monthly_traffic, budget_range,
                                referral_source, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data.get('name'), data.get('email'), data.get('phone'),
              data.get('company'), data.get('website'), data.get('service_interested'),
              data.get('monthly_traffic'), data.get('budget_range'),
              data.get('referral_source'), data.get('message')))
        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()
        return contact_id
    
    def insert_audit_request(self, data):
        """Insert audit request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_requests (website_url, email, industry, 
                                       competitor1, competitor2, competitor3)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('website_url'), data.get('email'), data.get('industry'),
              data.get('competitor1'), data.get('competitor2'), data.get('competitor3')))
        conn.commit()
        audit_id = cursor.lastrowid
        conn.close()
        return audit_id
    
    def subscribe_newsletter(self, email, source='website'):
        """Subscribe to newsletter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO newsletter_subscribers (email, source)
                VALUES (?, ?)
            ''', (email, source))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False  # Email already exists
        conn.close()
        return success
    
    def get_blog_posts(self, limit=None, category=None):
        """Get published blog posts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM blog_posts WHERE status='published'"
        if category:
            query += f" AND category='{category}'"
        query += " ORDER BY published_date DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        posts = cursor.fetchall()
        conn.close()
        return posts
    
    def get_blog_post_by_slug(self, slug):
        """Get single blog post by slug"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blog_posts WHERE slug=? AND status='published'", (slug,))
        post = cursor.fetchone()
        
        # Increment view count
        if post:
            cursor.execute("UPDATE blog_posts SET views = views + 1 WHERE slug=?", (slug,))
            conn.commit()
        
        conn.close()
        return post
    
    def get_testimonials(self, featured_only=False):
        """Get testimonials"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if featured_only:
            cursor.execute("SELECT * FROM testimonials WHERE featured=1 ORDER BY created_at DESC")
        else:
            cursor.execute("SELECT * FROM testimonials ORDER BY created_at DESC")
        
        testimonials = cursor.fetchall()
        conn.close()
        return testimonials
