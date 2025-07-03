# Custom Strut & Manufacturing Portfolio Website

A professional manufacturing portfolio website built with Hugo, inspired by customstrut.com/work. This website showcases custom roll forming and channel strut manufacturing capabilities with a modern, industrial design.

## Features

- **Responsive Design**: Mobile-first approach with responsive layouts
- **Professional Aesthetics**: Clean, industrial design with modern typography
- **Portfolio Showcase**: Filterable project gallery with detailed case studies
- **Service Pages**: Comprehensive service descriptions and capabilities
- **Contact Forms**: Professional contact forms for lead generation
- **Fast Performance**: Static site generation for optimal loading speeds

## Website Structure

### Homepage (`/`)
- Hero section with compelling value proposition
- Services overview with key capabilities
- Portfolio preview showcasing recent projects
- Statistics section highlighting experience and success
- Contact section with form and contact information

### Work/Portfolio Page (`/work/`)
- Filterable project gallery by category (Solar, Industrial, Commercial, Custom)
- Detailed project descriptions with client information
- Interactive filtering with smooth animations
- Call-to-action for new project inquiries

### Services Page (`/services/`)
- Detailed service descriptions
- Technical capabilities and specifications
- Quality assurance information
- Manufacturing process overview

### About Page (`/about/`)
- Company history and mission
- Team expertise and experience
- Facility capabilities
- Quality commitments

### Contact Page (`/contact/`)
- Multiple contact methods
- Business hours and location
- Contact form for project inquiries
- Industry expertise listing

## Technical Stack

- **Static Site Generator**: Hugo v0.121.0
- **Theme**: Custom portfolio theme
- **Styling**: Custom CSS with modern design principles
- **Fonts**: Inter font family for professional typography
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JS for interactions and animations

## Design Features

- **Color Scheme**: Professional blue and gray palette
- **Typography**: Inter font family for readability
- **Responsive Grid**: CSS Grid and Flexbox for layouts
- **Smooth Animations**: CSS transitions and JavaScript interactions
- **Mobile Navigation**: Hamburger menu for mobile devices
- **Card-based Design**: Modern card layouts for content organization

## Getting Started

### Prerequisites
- Hugo Extended v0.121.0 or later

### Installation
1. Clone this repository
2. Navigate to the project directory
3. Run `hugo server` to start the development server
4. Visit `http://localhost:1313` to view the website

### Development
- Content files are in the `content/` directory
- Templates are in `themes/portfolio/layouts/`
- Styling is in `static/css/style.css`
- JavaScript is in `static/js/main.js`

### Building for Production
```bash
hugo --minify
```

## Customization

### Content Updates
- Update company information in `hugo.toml`
- Modify content in markdown files in the `content/` directory
- Add new projects to the work page template

### Styling Changes
- Main styles are in `static/css/style.css`
- Color scheme can be updated by changing CSS variables
- Responsive breakpoints can be adjusted in media queries

### Adding Projects
Projects are currently hardcoded in the work template. To add new projects:
1. Edit `themes/portfolio/layouts/work/work.html`
2. Add new portfolio items with appropriate categories
3. Include project details, client information, and tags

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Performance Features

- Optimized CSS and JavaScript
- Responsive images with proper sizing
- Minimal external dependencies
- Fast static site generation
- Efficient caching strategies

## Deployment

This static site can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting provider

## License

This project is created for demonstration purposes. Customize as needed for your use case.

## Support

For questions about customization or deployment, please refer to the Hugo documentation at https://gohugo.io/documentation/.