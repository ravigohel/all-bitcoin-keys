# Vercel Deployment Guide

This guide explains how to deploy the All Bitcoin Private Key application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Vercel CLI** (optional): Install with `npm i -g vercel`

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./` (default)
   - Build Command: Leave empty (Vercel will auto-detect)
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

3. **Environment Variables** (if needed):
   - Add any environment variables in the Vercel dashboard
   - For this app, no additional environment variables are required

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-project-name.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new one
   - Confirm settings
   - Deploy

## Important Notes

### Serverless Limitations

- **Cold Starts**: First request may be slower due to serverless cold starts
- **Execution Time**: Vercel has a 10-second timeout for hobby plans
- **Memory**: Limited memory for large operations
- **Concurrent Requests**: May be limited on hobby plans

### Performance Considerations

- **Balance Scanning**: Large scans (500 pages) may timeout on Vercel
- **API Rate Limits**: Consider reducing concurrent threads for Vercel
- **Caching**: Vercel provides edge caching which can help with performance

### Recommended Settings for Vercel

Update `config.py` for Vercel deployment:

```python
# Reduce concurrent threads for Vercel
API_MAX_THREADS = 3  # Reduced from 10

# Reduce scan limits for Vercel
MAX_SEARCH_PAGES = 100  # Reduced from 1000
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Timeout Errors**: Reduce scan limits or concurrent operations
3. **Memory Issues**: Optimize for smaller operations
4. **Static Files**: Ensure templates are in the correct directory

### Debugging

1. **Check Vercel Logs**: Go to your project dashboard → Functions tab
2. **Test Locally**: Use `vercel dev` to test locally
3. **Check Build Logs**: Review build output for errors

## Custom Domain

1. **Add Domain**: In Vercel dashboard → Settings → Domains
2. **Configure DNS**: Point your domain to Vercel
3. **SSL**: Vercel automatically provides SSL certificates

## Monitoring

- **Analytics**: Available in Vercel dashboard
- **Performance**: Monitor function execution times
- **Errors**: Check function logs for issues

## Cost Considerations

- **Hobby Plan**: Free with limitations
- **Pro Plan**: $20/month for higher limits
- **Enterprise**: Custom pricing for large scale

For this application, the hobby plan should be sufficient for testing and small-scale usage.
