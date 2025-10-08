# Teams-Intercom Integration - Custom Bash Configuration

# Custom aliases for the project
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Python development aliases
alias py='python'
alias pip='python -m pip'
alias pytest='python -m pytest'
alias black='python -m black'
alias isort='python -m isort'
alias flake8='python -m flake8'
alias mypy='python -m mypy'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'
alias glog='git log --oneline --graph --decorate --all'

# Project specific aliases
alias rundev='uvicorn main:app --reload --host 0.0.0.0 --port 8000'
alias runprod='python main.py'
alias test='pytest -v'
alias testcov='pytest -v --cov=. --cov-report=html'
alias lint='flake8 . && pylint *.py'
alias format='black . && isort .'
alias typecheck='mypy .'
alias security='bandit -r . && safety check'
alias clean='find . -name "*.pyc" -delete && find . -name "__pycache__" -type d -exec rm -rf {} +'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'
alias dex='docker exec -it'

# Utility aliases
alias reload='source ~/.bashrc'
alias h='history'
alias c='clear'
alias path='echo -e ${PATH//:/\\n}'
alias ports='netstat -tuln'
alias json='python -m json.tool'

# Environment variables
export PYTHONPATH="$PWD:$PYTHONPATH"
export EDITOR='code'
export PAGER='less'

# Auto-activate virtual environment when entering project directory
function cd() {
    builtin cd "$@"
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi
}

# Activate virtual environment on shell start if in project directory
if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
fi

# Custom prompt with project info
PS1='\[\033[36m\][Teams-Intercom]\[\033[0m\] '$PS1

# Function to show project status
function project_status() {
    echo "🚀 Teams-Intercom Integration Status:"
    echo ""

    # Check if virtual environment is active
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "✅ Virtual environment: $(basename $VIRTUAL_ENV)"
    else
        echo "❌ Virtual environment: Not activated"
    fi

    # Check if .env file exists
    if [[ -f ".env" ]]; then
        echo "✅ Environment file: Found"
    else
        echo "❌ Environment file: Not found (.env)"
    fi

    # Check if dependencies are installed
    if python -c "import fastapi" 2>/dev/null; then
        echo "✅ Dependencies: Installed"
    else
        echo "❌ Dependencies: Not installed"
    fi

    # Check git status
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "✅ Git repository: $(git branch --show-current)"
        local changes=$(git status --porcelain | wc -l)
        if [[ $changes -gt 0 ]]; then
            echo "⚠️  Uncommitted changes: $changes files"
        else
            echo "✅ Working directory: Clean"
        fi
    fi

    echo ""
}

# Add project status to shell startup
project_status

echo "🎉 Teams-Intercom Integration shell environment loaded!"
echo "💡 Type 'project_status' to check the current status"
echo "📚 Type 'make help' to see available commands"
