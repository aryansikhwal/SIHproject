# Contributing to AttenSync

Thank you for your interest in contributing to AttenSync! This project aims to improve attendance management for rural schools across India.

## 🤝 How to Contribute

### 1. Fork the Repository
- Fork this repository to your GitHub account
- Clone your fork locally

### 2. Set Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/attensync.git
cd attensync

# Install dependencies
npm install

# Start development server
npm start
```

### 3. Make Your Changes

#### Code Style Guidelines
- Use functional components with React hooks
- Follow ESLint and Prettier configurations
- Write clean, readable code with meaningful variable names
- Add comments for complex logic

#### Commit Message Format
```
type(scope): description

Examples:
feat(attendance): add bulk attendance marking
fix(dashboard): resolve chart rendering issue
docs(readme): update installation instructions
style(components): improve button hover effects
```

### 4. Testing Your Changes

```bash
# Run tests (when available)
npm test

# Build to check for errors
npm run build

# Check for accessibility issues
# Test on mobile devices
# Verify translations work correctly
```

### 5. Submit a Pull Request

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to your branch: `git push origin feature/your-feature-name`
4. Open a Pull Request with:
   - Clear description of changes
   - Screenshots (if UI changes)
   - Testing instructions

## 🎯 Areas Where We Need Help

### High Priority
- [ ] **Backend Integration**: Flask API endpoints
- [ ] **Mobile Responsiveness**: Improve touch interactions
- [ ] **Performance**: Optimize for slower connections
- [ ] **Accessibility**: WCAG 2.1 compliance
- [ ] **Testing**: Unit and integration tests

### Medium Priority
- [ ] **New Features**: Biometric integration, SMS notifications
- [ ] **UI/UX**: Improve user experience for rural teachers
- [ ] **Documentation**: API documentation, user guides
- [ ] **Localization**: Additional regional languages

### Low Priority
- [ ] **Code Refactoring**: Optimize existing components
- [ ] **DevOps**: CI/CD pipeline setup
- [ ] **Monitoring**: Error tracking and analytics

## 🌐 Translation Contributions

We welcome translations into additional Indian languages!

### Adding a New Language

1. **Add translations** in `src/services/translationService.js`:
```javascript
export const staticTranslations = {
  en: { /* existing translations */ },
  hi: { /* existing translations */ },
  pa: { /* existing translations */ },
  bn: { /* your Bengali translations */ },
  // Add your language code and translations
};
```

2. **Update language options** in `src/contexts/LanguageContext.js`:
```javascript
languages: [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  // Add your language
]
```

3. **Test thoroughly** with the language switcher

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**: Browser, OS, device type
2. **Steps to reproduce**: Clear, numbered steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Screenshots**: If applicable
6. **Console errors**: Any JavaScript errors

Use this template:

```markdown
**Bug Description**
Brief description of the issue

**Environment**
- Browser: Chrome 91.0.4472.124
- OS: Windows 10
- Device: Desktop

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
A clear description of expected behavior

**Actual Behavior**
A clear description of what actually happens

**Screenshots**
Add screenshots if helpful

**Additional Context**
Any other context about the problem
```

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Propose a solution** if you have ideas
4. **Consider rural school context** in your suggestions

## 📋 Development Guidelines

### Code Quality
- Write self-documenting code
- Keep functions small and focused
- Use TypeScript-style JSDoc comments
- Prefer composition over inheritance

### Performance
- Optimize for slower internet connections
- Minimize bundle size
- Use lazy loading where appropriate
- Cache API responses when possible

### Accessibility
- Use semantic HTML elements
- Provide alt text for images
- Ensure keyboard navigation works
- Test with screen readers

### Rural School Considerations
- **Simple UI**: Avoid complex interactions
- **Clear Visual Hierarchy**: Important info should stand out
- **Touch-Friendly**: Large buttons for mobile devices
- **Offline Support**: Core features should work offline

## 🔒 Security Guidelines

- Never commit sensitive data (API keys, passwords)
- Validate all user inputs
- Use HTTPS for all API communications
- Follow OWASP security guidelines
- Report security issues privately

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bugs and feature requests
- **Email**: [your-email] for private matters

## 🏆 Recognition

Contributors will be:
- Listed in our README.md
- Mentioned in release notes
- Invited to join our contributor team

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and inclusive in all interactions.

---

Thank you for helping make education better for rural schools! 🌱📚
