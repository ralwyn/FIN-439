from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[4]/'Lab19'))
import panel
if __name__ == '__main__':
    sys.argv += ['--investor', 'Cathie Wood']
    panel.main()
