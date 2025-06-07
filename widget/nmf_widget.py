"""
NMF Heatmap Widget - anywidget wrapper for interactive NMF visualization.
"""
from __future__ import annotations
import anywidget
import plotly.graph_objects as go
from pathlib import Path
import traceback
from .nmf_plotting import create_nmf_heatmap_figure, create_empty_placeholder_figure


class NMFHeatmapWidget(anywidget.AnyWidget):
    """Plotly + anywidget interactive heat-map of NMF sample activities."""
    
    # Use external JavaScript file
    _esm = Path(__file__).parent / "nmf_widget.js"
    _css = Path(__file__).parent / "nmf_widget.css"

    def __init__(self, cfg_path: str | Path = "config.json"):
        """
        Initialize NMF heatmap widget.
        
        Parameters
        ----------
        cfg_path : str or Path
            Path to configuration JSON file containing data paths and settings
        """
        super().__init__()
        print("NMFHeatmapWidget: Initializing...")
        
        self._cfg_path = cfg_path
        
        try:
            self.figure = self._create_figure(cfg_path)
            print(f"NMFHeatmapWidget: Figure created successfully. Type: {type(self.figure)}")
        except Exception as e:
            print(f"NMFHeatmapWidget: Error during initialization: {e}")
            traceback.print_exc()
            self.figure = go.FigureWidget(create_empty_placeholder_figure())
            
        print("NMFHeatmapWidget: Initialization complete.")

    def _create_figure(self, cfg_path: str | Path) -> go.FigureWidget:
        """
        Create the Plotly figure for the widget.
        
        Parameters
        ----------
        cfg_path : str or Path
            Path to configuration file
            
        Returns
        -------
        go.FigureWidget
            Interactive Plotly figure widget
        """
        print(f"NMFHeatmapWidget: Creating figure from config: {cfg_path}")
        
        try:
            # Use the plotting module to create the figure
            fig = create_nmf_heatmap_figure(cfg_path)
            print("NMFHeatmapWidget: Figure created successfully.")
            
            # Return as FigureWidget for Jupyter integration
            return go.FigureWidget(fig)
            
        except Exception as e:
            print(f"NMFHeatmapWidget: Error creating figure: {e}")
            traceback.print_exc()
            
            # Return placeholder figure on error
            return go.FigureWidget(create_empty_placeholder_figure())

    def _repr_mimebundle_(self, **kwargs):
        """Ensure the figure is displayed when the widget is shown."""
        if hasattr(self, 'figure') and self.figure is not None:
            return self.figure._repr_mimebundle_(**kwargs)
        return {}

    def refresh(self, cfg_path: str | Path = None):
        """Refresh the widget with new data."""
        if cfg_path is None:
            cfg_path = self._cfg_path
        
        try:
            self.figure = self._create_figure(cfg_path)
            print("NMFHeatmapWidget: Figure refreshed successfully.")
        except Exception as e:
            print(f"NMFHeatmapWidget: Error refreshing figure: {e}")
            traceback.print_exc()

    def save_figure(self, filename: str, **kwargs):
        """Save the figure to file."""
        if self.figure:
            if filename.endswith('.html'):
                self.figure.write_html(filename, **kwargs)
            else:
                self.figure.write_image(filename, **kwargs)
            print(f"NMFHeatmapWidget: Figure saved to {filename}")
        else:
            print("NMFHeatmapWidget: No figure to save.")


def create_nmf_widget(cfg_path: str | Path = "config.json") -> NMFHeatmapWidget:
    """Create an NMF heatmap widget."""
    return NMFHeatmapWidget(cfg_path)
