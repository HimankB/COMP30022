#!/bin/bash

# Development Setup Script for Legal AI Project

set -e

echo "🚀 Setting up Legal AI Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment files from examples if they don't exist
echo "📁 Setting up environment files..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env from template"
fi

if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ Created frontend/.env.local from template"
fi

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env from template"
fi

if [ ! -f ai-service/.env ]; then
    cp ai-service/.env.example ai-service/.env
    echo "✅ Created ai-service/.env from template"
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p ai-service/data/documents
mkdir -p ai-service/data/vector_db

echo "🐳 Building and starting Docker containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend is not responding"
fi

if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Backend API is running at http://localhost:5000"
else
    echo "❌ Backend API is not responding"
fi

if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ AI Service is running at http://localhost:8000"
else
    echo "❌ AI Service is not responding"
fi

echo ""
echo "🎉 Setup complete! Your development environment is ready."
echo ""
echo "Next steps:"
echo "1. Edit the .env files with your actual API keys and configuration"
echo "2. Visit http://localhost:3000 to access the application"
echo "3. Check the logs with: docker-compose logs -f [service-name]"
echo ""
echo "Useful commands:"
echo "  docker-compose down          # Stop all services"
echo "  docker-compose logs -f       # View all logs"
echo "  docker-compose build         # Rebuild all services"
echo ""