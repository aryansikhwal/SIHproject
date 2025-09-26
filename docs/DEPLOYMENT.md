# 🚀 AttenSync Deployment Guide

This guide covers different deployment options for AttenSync, optimized for rural school environments.

## 📋 Prerequisites

- Node.js 16+ and npm
- Git
- Domain name (optional)
- Hosting service account

## 🌐 Deployment Options

### 1. Netlify (Recommended for Frontend)

**Pros**: Free tier, automatic deployments, CDN, HTTPS
**Cons**: Frontend only (needs separate backend)

#### Steps:
1. **Push to GitHub**: Upload your code to GitHub
2. **Connect Netlify**: 
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
3. **Configure Build**:
   - Build command: `npm run build`
   - Publish directory: `build`
4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend-url.com
   ```
5. **Custom Domain**: Add your domain in site settings

### 2. Vercel

**Pros**: Free tier, excellent performance, automatic deployments
**Cons**: Frontend only

#### Steps:
1. Install Vercel CLI: `npm i -g vercel`
2. In project directory: `vercel`
3. Follow the prompts
4. Set environment variables in Vercel dashboard

### 3. GitHub Pages

**Pros**: Free for public repositories
**Cons**: Static hosting only, limited features

#### Steps:
1. Install gh-pages: `npm install --save-dev gh-pages`
2. Add to package.json:
   ```json
   {
     "homepage": "https://yourusername.github.io/attensync",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```
3. Deploy: `npm run deploy`

### 4. Self-Hosting (For Rural Areas)

**Pros**: Full control, can work offline, no external dependencies
**Cons**: Requires technical setup, maintenance

#### Option A: Local Server Setup
```bash
# Build the project
npm run build

# Serve using a simple HTTP server
npm install -g serve
serve -s build -p 3000
```

#### Option B: Docker Deployment
```dockerfile
# Dockerfile
FROM node:16-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔧 Environment Configuration

### Production Environment Variables
Create a `.env.production` file:
```bash
# API Configuration
REACT_APP_API_URL=https://your-backend-api.com
REACT_APP_ENV=production

# Features
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ENABLE_OFFLINE=true

# School Configuration (Optional)
REACT_APP_SCHOOL_NAME="Your School Name"
REACT_APP_SCHOOL_ID="SCH001"
```

### Development vs Production
```bash
# Development
REACT_APP_API_URL=http://localhost:5000

# Production
REACT_APP_API_URL=https://api.yourschool.edu.in
```

## 📱 Mobile Deployment

### Progressive Web App (PWA)
AttenSync is PWA-ready. Users can:
1. Visit the website on mobile
2. Tap "Add to Home Screen"
3. Use like a native app

### Mobile App (Future)
- React Native version planned
- Same codebase, native performance
- Offline-first architecture

## 🏫 Rural School Specific Deployments

### 1. Offline-First Setup
```bash
# Enable service worker for offline functionality
# Add to public/sw.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('attensync-v1').then((cache) => {
      return cache.addAll([
        '/',
        '/static/js/bundle.js',
        '/static/css/main.css',
        // Add other critical files
      ]);
    })
  );
});
```

### 2. Low-Bandwidth Optimization
```json
// webpack.config.js optimization
{
  "optimization": {
    "splitChunks": {
      "chunks": "all",
      "maxSize": 200000
    }
  }
}
```

### 3. Local Network Deployment
For schools with local networks but limited internet:

```bash
# Set up local network access
npm run build
serve -s build -p 80 --host 0.0.0.0

# Access from any device on network:
# http://192.168.1.100 (replace with server IP)
```

## 🔒 Security Configuration

### HTTPS Setup
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name yourschool.edu.in;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
```

### Security Headers
```nginx
# Add to nginx.conf
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## 📊 Performance Monitoring

### Google Analytics Setup
```javascript
// Add to public/index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Error Monitoring
```bash
# Install Sentry for error tracking
npm install @sentry/react @sentry/tracing
```

## 🚨 Troubleshooting

### Common Issues

**Build Fails**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**API Connection Issues**
- Check CORS settings on backend
- Verify API URL in environment variables
- Test API endpoints independently

**Mobile Issues**
- Test on actual devices, not just browser dev tools
- Check touch interactions
- Verify responsive breakpoints

### Performance Issues
```bash
# Analyze bundle size
npm install -g webpack-bundle-analyzer
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

## 📞 Support

For deployment issues:
- Create an issue on GitHub
- Check our troubleshooting wiki
- Contact support team

## 🎯 Deployment Checklist

### Pre-Deployment
- [ ] All features tested locally
- [ ] Mobile responsiveness verified
- [ ] All languages working correctly
- [ ] API integration tested
- [ ] Performance optimized
- [ ] Security headers configured

### Post-Deployment
- [ ] SSL certificate working
- [ ] All pages load correctly
- [ ] API connections working
- [ ] Mobile app functionality
- [ ] Error monitoring setup
- [ ] Analytics configured
- [ ] Backup procedures in place

### Rural School Specific
- [ ] Works with slow internet
- [ ] Offline functionality tested
- [ ] Local network access verified
- [ ] Simple URL for teachers
- [ ] Mobile-first interface working
- [ ] All languages displaying correctly

---

**Need help with deployment?** 
Create an issue on GitHub with the `deployment` label and we'll help you get AttenSync running for your school! 🌱📚
