import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from tkinter.colorchooser import askcolor
from datetime import datetime, timedelta
import json
import os
import random
import webbrowser

class UltimateTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Empress To-Do Manager 👑")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Custom color scheme
        self.colors = {
            'dark_bg': '#1a1a1a',
            'light_bg': '#2d2d2d',
            'accent_dark': '#8b0000',
            'accent_light': '#ff4d4d',
            'text': '#f0f0f0',
            'highlight': '#ff9999',
            'completed': '#4d4d4d',
            'selected': '#660000'
        }
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # App data
        self.tasks = []
        self.categories = ['💼 Work', '🏠 Personal', '🎓 Study', '❤️ Health', '🛒 Shopping', '🎉 Fun']
        self.priorities = ['🔥 Critical', '⚠️ High', '🔼 Medium', '🔽 Low', '🌱 Chill']
        self.emoji_list = ['🌸', '✨', '💖', '🦋', '🍒', '🎀', '👑', '💄', '👠', '👜']
        
        # Load saved data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
        # Start with a motivational quote
        self.show_daily_quote()
        
    def configure_styles(self):
        """Configure all widget styles"""
        # Main styles
        self.style.configure('.', 
                            background=self.colors['dark_bg'],
                            foreground=self.colors['text'],
                            font=('Segoe UI', 10))
        
        # Frame styles
        self.style.configure('Dark.TFrame', background=self.colors['dark_bg'])
        self.style.configure('Light.TFrame', background=self.colors['light_bg'])
        
        # Label styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 18, 'bold'),
                           foreground=self.colors['accent_light'],
                           background=self.colors['dark_bg'])
        
        self.style.configure('Subtitle.TLabel', 
                           font=('Segoe UI', 12),
                           foreground=self.colors['highlight'],
                           background=self.colors['dark_bg'])
        
        # Button styles
        self.style.configure('Accent.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           foreground=self.colors['text'],
                           background=self.colors['accent_dark'],
                           borderwidth=1)
        
        self.style.map('Accent.TButton',
                     foreground=[('pressed', self.colors['text']), 
                                ('active', self.colors['text'])],
                     background=[('pressed', self.colors['accent_light']), 
                                ('active', self.colors['accent_light'])])
        
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 9),
                           foreground=self.colors['text'],
                           background=self.colors['light_bg'],
                           borderwidth=0)
        
        # Entry styles
        self.style.configure('Dark.TEntry',
                           fieldbackground=self.colors['light_bg'],
                           foreground=self.colors['text'],
                           insertcolor=self.colors['text'],
                           bordercolor=self.colors['accent_dark'],
                           lightcolor=self.colors['accent_dark'],
                           darkcolor=self.colors['accent_dark'])
        
        # Combobox styles
        self.style.configure('Dark.TCombobox',
                           fieldbackground=self.colors['light_bg'],
                           foreground=self.colors['text'],
                           background=self.colors['light_bg'])
        
        self.style.map('Dark.TCombobox',
                     fieldbackground=[('readonly', self.colors['light_bg'])],
                     selectbackground=[('readonly', self.colors['accent_dark'])],
                     selectforeground=[('readonly', self.colors['text'])])
        
        # Treeview styles
        self.style.configure('Custom.Treeview',
                           background=self.colors['light_bg'],
                           foreground=self.colors['text'],
                           fieldbackground=self.colors['light_bg'],
                           borderwidth=0,
                           rowheight=25)
        
        self.style.configure('Custom.Treeview.Heading',
                           background=self.colors['accent_dark'],
                           foreground=self.colors['text'],
                           font=('Segoe UI', 10, 'bold'),
                           relief='flat')
        
        self.style.map('Custom.Treeview',
                     background=[('selected', self.colors['selected'])],
                     foreground=[('selected', self.colors['text'])])
        
        # Scrollbar styles
        self.style.configure('Dark.Vertical.TScrollbar',
                           background=self.colors['dark_bg'],
                           troughcolor=self.colors['dark_bg'],
                           bordercolor=self.colors['dark_bg'],
                           arrowcolor=self.colors['accent_light'],
                           gripcount=0)
        
        self.style.map('Dark.Vertical.TScrollbar',
                     background=[('active', self.colors['accent_light'])])
        
        # Notebook styles
        self.style.configure('Dark.TNotebook',
                           background=self.colors['dark_bg'],
                           bordercolor=self.colors['dark_bg'])
        
        self.style.configure('Dark.TNotebook.Tab',
                           background=self.colors['dark_bg'],
                           foreground=self.colors['text'],
                           lightcolor=self.colors['dark_bg'],
                           bordercolor=self.colors['dark_bg'],
                           padding=[10, 5],
                           font=('Segoe UI', 10))
        
        self.style.map('Dark.TNotebook.Tab',
                     background=[('selected', self.colors['accent_dark'])],
                     foreground=[('selected', self.colors['text'])])
        
        # Checkbutton styles
        self.style.configure('Dark.TCheckbutton',
                           background=self.colors['dark_bg'],
                           foreground=self.colors['text'],
                           indicatorbackground=self.colors['light_bg'],
                           indicatordiameter=15)
        
        self.style.map('Dark.TCheckbutton',
                     indicatorbackground=[('selected', self.colors['accent_light'])])
        
        # Progressbar styles
        self.style.configure('Custom.Horizontal.TProgressbar',
                           thickness=20,
                           troughcolor=self.colors['light_bg'],
                           background=self.colors['accent_light'],
                           lightcolor=self.colors['accent_light'],
                           darkcolor=self.colors['accent_dark'],
                           bordercolor=self.colors['dark_bg'])
    
    def setup_ui(self):
        """Set up the main user interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Main content area
        self.content_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sidebar
        self.setup_sidebar()
        
        # Main task area
        self.setup_task_area()
        
        # Status bar
        self.setup_status_bar()
        
        # Apply custom fonts
        self.apply_custom_fonts()
        
        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()
    
    def setup_header(self):
        """Set up the header with title and quick actions"""
        header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # App title with emoji
        title_emoji = random.choice(self.emoji_list)
        title_label = ttk.Label(header_frame, 
                               text=f"{title_emoji} Empress To-Do Manager {title_emoji}", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Quick action buttons
        button_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        button_frame.pack(side=tk.RIGHT)
        
        self.quick_add_btn = ttk.Button(button_frame, text="⚡ Quick Add", 
                                      style='Secondary.TButton',
                                      command=self.quick_add_task)
        self.quick_add_btn.pack(side=tk.LEFT, padx=5)
        
        self.search_btn = ttk.Button(button_frame, text="🔍 Search", 
                                   style='Secondary.TButton',
                                   command=self.toggle_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_btn = ttk.Button(button_frame, text="📊 Stats", 
                                  style='Secondary.TButton',
                                  command=self.show_stats)
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        self.settings_btn = ttk.Button(button_frame, text="⚙️ Settings", 
                                     style='Secondary.TButton',
                                     command=self.open_settings)
        self.settings_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_sidebar(self):
        """Set up the sidebar with navigation and filters"""
        sidebar_frame = ttk.Frame(self.content_frame, style='Light.TFrame', width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Navigation
        nav_frame = ttk.Frame(sidebar_frame, style='Light.TFrame')
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(nav_frame, text="🌺 Navigation", style='Subtitle.TLabel').pack(anchor=tk.W, pady=5)
        
        self.view_all_btn = ttk.Button(nav_frame, text="👁️ View All Tasks", 
                                     style='Secondary.TButton',
                                     command=lambda: self.filter_tasks('all'))
        self.view_all_btn.pack(fill=tk.X, pady=2)
        
        self.view_today_btn = ttk.Button(nav_frame, text="📅 Today's Tasks", 
                                       style='Secondary.TButton',
                                       command=lambda: self.filter_tasks('today'))
        self.view_today_btn.pack(fill=tk.X, pady=2)
        
        self.view_upcoming_btn = ttk.Button(nav_frame, text="⏳ Upcoming", 
                                          style='Secondary.TButton',
                                          command=lambda: self.filter_tasks('upcoming'))
        self.view_upcoming_btn.pack(fill=tk.X, pady=2)
        
        self.view_completed_btn = ttk.Button(nav_frame, text="✅ Completed", 
                                           style='Secondary.TButton',
                                           command=lambda: self.filter_tasks('completed'))
        self.view_completed_btn.pack(fill=tk.X, pady=2)
        
        # Categories filter
        cat_frame = ttk.Frame(sidebar_frame, style='Light.TFrame')
        cat_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(cat_frame, text="🏷️ Categories", style='Subtitle.TLabel').pack(anchor=tk.W, pady=5)
        
        self.category_buttons = []
        for category in self.categories:
            btn = ttk.Button(cat_frame, text=category, 
                            style='Secondary.TButton',
                            command=lambda c=category: self.filter_tasks('category', c))
            btn.pack(fill=tk.X, pady=2)
            self.category_buttons.append(btn)
        
        # Priority filter
        prio_frame = ttk.Frame(sidebar_frame, style='Light.TFrame')
        prio_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(prio_frame, text="🚨 Priority", style='Subtitle.TLabel').pack(anchor=tk.W, pady=5)
        
        self.priority_buttons = []
        for priority in self.priorities:
            btn = ttk.Button(prio_frame, text=priority, 
                            style='Secondary.TButton',
                            command=lambda p=priority: self.filter_tasks('priority', p))
            btn.pack(fill=tk.X, pady=2)
            self.priority_buttons.append(btn)
    
    def setup_task_area(self):
        """Set up the main task display and management area"""
        task_main_frame = ttk.Frame(self.content_frame, style='Dark.TFrame')
        task_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Search bar (hidden by default)
        self.search_frame = ttk.Frame(task_main_frame, style='Light.TFrame')
        
        self.search_entry = ttk.Entry(self.search_frame, style='Dark.TEntry')
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        search_btn = ttk.Button(self.search_frame, text="🔍 Search", 
                              style='Accent.TButton',
                              command=self.perform_search)
        search_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_search_btn = ttk.Button(self.search_frame, text="✖️", 
                                     style='Secondary.TButton',
                                     command=self.toggle_search)
        cancel_search_btn.pack(side=tk.RIGHT)
        
        # Task controls
        controls_frame = ttk.Frame(task_main_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_task_btn = ttk.Button(controls_frame, text="➕ Add New Task", 
                                     style='Accent.TButton',
                                     command=self.open_add_task_dialog)
        self.add_task_btn.pack(side=tk.LEFT)
        
        self.edit_task_btn = ttk.Button(controls_frame, text="✏️ Edit", 
                                      style='Secondary.TButton',
                                      command=self.edit_selected_task,
                                      state=tk.DISABLED)
        self.edit_task_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_task_btn = ttk.Button(controls_frame, text="🗑️ Delete", 
                                        style='Secondary.TButton',
                                        command=self.delete_selected_task,
                                        state=tk.DISABLED)
        self.delete_task_btn.pack(side=tk.LEFT, padx=5)
        
        self.complete_task_btn = ttk.Button(controls_frame, text="✓ Complete", 
                                          style='Secondary.TButton',
                                          command=self.toggle_task_completion,
                                          state=tk.DISABLED)
        self.complete_task_btn.pack(side=tk.LEFT, padx=5)
        
        # Task view tabs
        self.notebook = ttk.Notebook(task_main_frame, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # List view tab
        self.list_view_frame = ttk.Frame(self.notebook, style='Light.TFrame')
        self.notebook.add(self.list_view_frame, text="📋 List View")
        
        self.setup_list_view()
        
        # Board view tab
        self.board_view_frame = ttk.Frame(self.notebook, style='Light.TFrame')
        self.notebook.add(self.board_view_frame, text="📌 Board View")
        
        # Calendar view tab
        self.calendar_view_frame = ttk.Frame(self.notebook, style='Light.TFrame')
        self.notebook.add(self.calendar_view_frame, text="📅 Calendar View")
        
        # Progress tab
        self.progress_frame = ttk.Frame(self.notebook, style='Light.TFrame')
        self.notebook.add(self.progress_frame, text="📊 Progress")
        
        # Set up all views
        self.setup_board_view()
        self.setup_calendar_view()
        self.setup_progress_view()
        
        # Bind notebook tab change
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def setup_list_view(self):
        """Set up the list view of tasks"""
        # Treeview for tasks
        self.tree = ttk.Treeview(self.list_view_frame, style='Custom.Treeview',
                                columns=('id', 'completed', 'title', 'due_date', 'priority', 'category'),
                                show='headings', selectmode='browse')
        
        # Configure columns
        self.tree.column('id', width=0, stretch=tk.NO)  # Hidden ID column
        self.tree.column('completed', width=30, anchor=tk.CENTER)
        self.tree.column('title', width=300, anchor=tk.W)
        self.tree.column('due_date', width=120, anchor=tk.CENTER)
        self.tree.column('priority', width=120, anchor=tk.CENTER)
        self.tree.column('category', width=120, anchor=tk.CENTER)
        
        # Configure headings
        self.tree.heading('completed', text='✓')
        self.tree.heading('title', text='Task')
        self.tree.heading('due_date', text='Due Date')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('category', text='Category')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_view_frame, style='Dark.Vertical.TScrollbar',
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_task_selected)
        
        # Double click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_task())
        
        # Populate with tasks
        self.update_task_list()
    
    def setup_board_view(self):
        """Set up the kanban-style board view"""
        # Create columns for different statuses
        board_columns = [
            {'id': 'todo', 'title': '📝 To Do', 'color': '#8b0000'},
            {'id': 'in_progress', 'title': '⏳ In Progress', 'color': '#cc5500'},
            {'id': 'done', 'title': '✅ Done', 'color': '#006400'}
        ]
        
        self.board_frames = {}
        self.board_lists = {}
        
        # Create a frame for each column
        for col in board_columns:
            frame = ttk.Frame(self.board_view_frame, style='Light.TFrame')
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Column header
            header = ttk.Frame(frame, style='Light.TFrame')
            header.pack(fill=tk.X)
            
            label = ttk.Label(header, text=col['title'], style='Subtitle.TLabel')
            label.pack(side=tk.LEFT, padx=5, pady=5)
            
            count_label = ttk.Label(header, text="0", style='Subtitle.TLabel')
            count_label.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Task list
            canvas = tk.Canvas(frame, bg=self.colors['light_bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, style='Dark.Vertical.TScrollbar',
                                    command=canvas.yview)
            
            task_frame = ttk.Frame(canvas, style='Light.TFrame')
            task_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=task_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Store references
            self.board_frames[col['id']] = {
                'frame': frame,
                'task_frame': task_frame,
                'count_label': count_label
            }
            self.board_lists[col['id']] = []
        
        # Update board view
        self.update_board_view()
    
    def setup_calendar_view(self):
        """Set up the calendar view of tasks"""
        # Month and year navigation
        nav_frame = ttk.Frame(self.calendar_view_frame, style='Light.TFrame')
        nav_frame.pack(fill=tk.X, pady=5)
        
        self.prev_month_btn = ttk.Button(nav_frame, text="◀", 
                                       style='Secondary.TButton',
                                       command=self.prev_month)
        self.prev_month_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_year_label = ttk.Label(nav_frame, text="", style='Subtitle.TLabel')
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        self.next_month_btn = ttk.Button(nav_frame, text="▶", 
                                       style='Secondary.TButton',
                                       command=self.next_month)
        self.next_month_btn.pack(side=tk.RIGHT, padx=5)
        
        # Calendar grid
        self.calendar_frame = ttk.Frame(self.calendar_view_frame, style='Light.TFrame')
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize with current month
        self.current_date = datetime.now()
        self.update_calendar_view()
    
    def setup_progress_view(self):
        """Set up the progress tracking view"""
        # Stats overview
        stats_frame = ttk.Frame(self.progress_frame, style='Light.TFrame')
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Completion rate
        ttk.Label(stats_frame, text="📈 Completion Rate", style='Subtitle.TLabel').pack(anchor=tk.W)
        
        self.completion_rate = ttk.Progressbar(stats_frame, style='Custom.Horizontal.TProgressbar',
                                             length=200, mode='determinate')
        self.completion_rate.pack(fill=tk.X, pady=5)
        
        # Tasks by priority
        ttk.Label(stats_frame, text="🚨 Tasks by Priority", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        self.priority_bars = {}
        for priority in self.priorities:
            frame = ttk.Frame(stats_frame, style='Light.TFrame')
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=priority, width=15, style='Subtitle.TLabel').pack(side=tk.LEFT)
            
            bar = ttk.Progressbar(frame, style='Custom.Horizontal.TProgressbar',
                                length=100, mode='determinate')
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            count_label = ttk.Label(frame, text="0", style='Subtitle.TLabel')
            count_label.pack(side=tk.RIGHT, padx=5)
            
            self.priority_bars[priority] = {'bar': bar, 'label': count_label}
        
        # Recent activity
        ttk.Label(stats_frame, text="🔄 Recent Activity", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        self.activity_log = scrolledtext.ScrolledText(stats_frame, 
                                                    bg=self.colors['light_bg'],
                                                    fg=self.colors['text'],
                                                    insertbackground=self.colors['text'],
                                                    wrap=tk.WORD,
                                                    font=('Segoe UI', 9))
        self.activity_log.pack(fill=tk.BOTH, expand=True, pady=5)
        self.activity_log.configure(state='disabled')
        
        # Update progress view
        self.update_progress_view()
    
    def setup_status_bar(self):
        """Set up the status bar at the bottom"""
        self.status_bar = ttk.Frame(self.main_frame, style='Light.TFrame', height=25)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 10))
        
        self.task_count_label = ttk.Label(self.status_bar, text="Tasks: 0", style='Subtitle.TLabel')
        self.task_count_label.pack(side=tk.LEFT, padx=10)
        
        self.completed_count_label = ttk.Label(self.status_bar, text="Completed: 0", style='Subtitle.TLabel')
        self.completed_count_label.pack(side=tk.LEFT, padx=10)
        
        self.selected_label = ttk.Label(self.status_bar, text="Selected: None", style='Subtitle.TLabel')
        self.selected_label.pack(side=tk.LEFT, padx=10)
        
        self.version_label = ttk.Label(self.status_bar, text="Empress To-Do v1.0", style='Subtitle.TLabel')
        self.version_label.pack(side=tk.RIGHT, padx=10)
        
        # Update status bar
        self.update_status_bar()
    
    def apply_custom_fonts(self):
        """Apply custom fonts to specific widgets"""
        try:
            # Try to use the Segoe UI Emoji font if available
            emoji_font = font.Font(family="Segoe UI Emoji", size=12)
            self.tree.tag_configure('emoji', font=emoji_font)
        except:
            pass
    
    def setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.open_add_task_dialog())
        self.root.bind('<Control-f>', lambda e: self.toggle_search())
        self.root.bind('<Delete>', lambda e: self.delete_selected_task())
        self.root.bind('<Control-s>', lambda e: self.save_data())
    
    # ==============================================
    # Task Management Methods
    # ==============================================
    
    def add_task(self, title, description="", due_date=None, priority="🔼 Medium", category="💼 Work"):
        """Add a new task to the list"""
        task_id = len(self.tasks) + 1
        completed = False
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'category': category,
            'completed': completed,
            'created_at': created_at,
            'completed_at': None,
            'status': 'todo'
        }
        
        self.tasks.append(task)
        self.update_all_views()
        self.log_activity(f"Added task: {title}")
        
        return task_id
    
    def edit_task(self, task_id, **kwargs):
        """Edit an existing task"""
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if task:
            for key, value in kwargs.items():
                if key in task and key != 'id':  # Don't allow changing the ID
                    task[key] = value
            
            self.update_all_views()
            self.log_activity(f"Updated task: {task['title']}")
            return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task from the list"""
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if task:
            self.tasks.remove(task)
            self.update_all_views()
            self.log_activity(f"Deleted task: {task['title']}")
            return True
        return False
    
    def toggle_task_completion(self, task_id=None):
        """Toggle completion status of a task"""
        if task_id is None:
            selected = self.get_selected_task()
            if selected:
                task_id = selected['id']
        
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if task:
            task['completed'] = not task['completed']
            task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M") if task['completed'] else None
            task['status'] = 'done' if task['completed'] else 'todo'
            
            self.update_all_views()
            action = "Completed" if task['completed'] else "Marked incomplete"
            self.log_activity(f"{action} task: {task['title']}")
            return True
        return False
    
    def get_selected_task(self):
        """Get the currently selected task"""
        if self.notebook.index(self.notebook.select()) == 0:  # List view
            selected = self.tree.selection()
            if selected:
                item = self.tree.item(selected[0])
                task_id = int(item['values'][0])
                return next((t for t in self.tasks if t['id'] == task_id), None)
        return None
    
    # ==============================================
    # UI Update Methods
    # ==============================================
    
    def update_all_views(self):
        """Update all task views"""
        self.update_task_list()
        self.update_board_view()
        self.update_calendar_view()
        self.update_progress_view()
        self.update_status_bar()
    
    def update_task_list(self, tasks=None):
        """Update the list view with tasks"""
        if tasks is None:
            tasks = self.tasks
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add tasks to the treeview
        for task in sorted(tasks, key=lambda x: (
            x['completed'], 
            self.priorities.index(x['priority']) if x['priority'] in self.priorities else len(self.priorities),
            x['due_date'] or '9999-12-31'
        )):
            completed = "✓" if task['completed'] else ""
            due_date = task['due_date'] if task['due_date'] else ""
            
            values = (
                task['id'],
                completed,
                task['title'],
                due_date,
                task['priority'],
                task['category']
            )
            
            item = self.tree.insert('', tk.END, values=values)
            
            # Style completed tasks differently
            if task['completed']:
                self.tree.item(item, tags=('completed',))
                self.tree.tag_configure('completed', foreground=self.colors['completed'])
    
    def update_board_view(self):
        """Update the kanban board view"""
        # Clear all task frames
        for col in self.board_frames.values():
            for widget in col['task_frame'].winfo_children():
                widget.destroy()
            col['count_label'].config(text="0")
        
        # Add tasks to appropriate columns
        for task in self.tasks:
            status = task['status']
            if status in self.board_frames:
                frame = self.board_frames[status]['task_frame']
                count_label = self.board_frames[status]['count_label']
                
                # Create task card
                card = ttk.Frame(frame, style='Light.TFrame', borderwidth=1, relief='solid')
                card.pack(fill=tk.X, padx=5, pady=5)
                
                # Task title
                title_frame = ttk.Frame(card, style='Light.TFrame')
                title_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
                
                checkbox = ttk.Checkbutton(title_frame, style='Dark.TCheckbutton',
                                         variable=tk.IntVar(value=1 if task['completed'] else 0),
                                         command=lambda t=task: self.toggle_task_completion(t['id']))
                checkbox.pack(side=tk.LEFT)
                
                title = ttk.Label(title_frame, text=task['title'], style='Subtitle.TLabel')
                title.pack(side=tk.LEFT, padx=5)
                
                # Task details
                details_frame = ttk.Frame(card, style='Light.TFrame')
                details_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
                
                ttk.Label(details_frame, text=task['priority'], style='Subtitle.TLabel').pack(side=tk.LEFT)
                ttk.Label(details_frame, text=task['category'], style='Subtitle.TLabel').pack(side=tk.RIGHT)
                
                # Update count
                current_count = int(count_label.cget("text"))
                count_label.config(text=str(current_count + 1))
    
    def update_calendar_view(self):
        """Update the calendar view"""
        # Clear current calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Set month/year label
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))
        
        # Get first day of month and days in month
        first_day = self.current_date.replace(day=1)
        days_in_month = (first_day.replace(month=first_day.month % 12 + 1, day=1) - 
                        timedelta(days=1)).day
        
        # Create day headers
        headers = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, header in enumerate(headers):
            label = ttk.Label(self.calendar_frame, text=header, style='Subtitle.TLabel',
                            width=10, anchor=tk.CENTER)
            label.grid(row=0, column=i, padx=2, pady=2)
        
        # Calculate starting position
        start_pos = first_day.weekday()  # Monday is 0, Sunday is 6
        
        # Create calendar grid
        day_num = 1
        for row in range(1, 7):
            for col in range(7):
                if row == 1 and col < start_pos:
                    # Empty cell before first day
                    ttk.Frame(self.calendar_frame, style='Light.TFrame', 
                             width=100, height=80).grid(row=row, column=col, padx=2, pady=2)
                elif day_num <= days_in_month:
                    # Day cell with tasks
                    day_frame = ttk.Frame(self.calendar_frame, style='Light.TFrame',
                                        borderwidth=1, relief='solid')
                    day_frame.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                    
                    # Day number
                    day_label = ttk.Label(day_frame, text=str(day_num), style='Subtitle.TLabel')
                    day_label.pack(anchor=tk.NW, padx=5, pady=5)
                    
                    # Get tasks for this day
                    current_date_str = self.current_date.replace(day=day_num).strftime("%Y-%m-%d")
                    day_tasks = [t for t in self.tasks if t['due_date'] == current_date_str]
                    
                    if day_tasks:
                        # Show task count
                        task_count = ttk.Label(day_frame, 
                                              text=f"{len(day_tasks)} task{'s' if len(day_tasks) != 1 else ''}",
                                              style='Subtitle.TLabel')
                        task_count.pack(anchor=tk.SW, padx=5, pady=5)
                    
                    day_num += 1
                else:
                    # Empty cell after last day
                    ttk.Frame(self.calendar_frame, style='Light.TFrame', 
                             width=100, height=80).grid(row=row, column=col, padx=2, pady=2)
        
        # Configure grid weights
        for col in range(7):
            self.calendar_frame.grid_columnconfigure(col, weight=1)
        for row in range(1, 7):
            self.calendar_frame.grid_rowconfigure(row, weight=1)
    
    def update_progress_view(self):
        """Update the progress statistics view"""
        # Calculate completion rate
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        self.completion_rate['value'] = completion_rate
        
        # Update priority bars
        for priority in self.priorities:
            tasks_in_priority = [t for t in self.tasks if t['priority'] == priority]
            completed_in_priority = len([t for t in tasks_in_priority if t['completed']])
            total_in_priority = len(tasks_in_priority)
            
            completion_rate = (completed_in_priority / total_in_priority * 100) if total_in_priority > 0 else 0
            
            self.priority_bars[priority]['bar']['value'] = completion_rate
            self.priority_bars[priority]['label'].config(
                text=f"{completed_in_priority}/{total_in_priority}")
    
    def update_status_bar(self):
        """Update the status bar information"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        
        self.task_count_label.config(text=f"Tasks: {total_tasks}")
        self.completed_count_label.config(text=f"Completed: {completed_tasks}")
        
        selected = self.get_selected_task()
        if selected:
            self.selected_label.config(text=f"Selected: {selected['title']}")
            # Update button states
            self.edit_task_btn.config(state=tk.NORMAL)
            self.delete_task_btn.config(state=tk.NORMAL)
            self.complete_task_btn.config(state=tk.NORMAL)
            
            # Update complete button text based on current state
            btn_text = "✓ Complete" if not selected['completed'] else "↻ Undo"
            self.complete_task_btn.config(text=btn_text)
        else:
            self.selected_label.config(text="Selected: None")
            self.edit_task_btn.config(state=tk.DISABLED)
            self.delete_task_btn.config(state=tk.DISABLED)
            self.complete_task_btn.config(state=tk.DISABLED)
    
    # ==============================================
    # Filtering and Searching
    # ==============================================
    
    def filter_tasks(self, filter_type, filter_value=None):
        """Filter tasks based on criteria"""
        if filter_type == 'all':
            filtered_tasks = self.tasks
        elif filter_type == 'today':
            today = datetime.now().strftime("%Y-%m-%d")
            filtered_tasks = [t for t in self.tasks if t['due_date'] == today]
        elif filter_type == 'upcoming':
            today = datetime.now().strftime("%Y-%m-%d")
            filtered_tasks = [t for t in self.tasks if t['due_date'] and t['due_date'] >= today]
        elif filter_type == 'completed':
            filtered_tasks = [t for t in self.tasks if t['completed']]
        elif filter_type == 'category':
            filtered_tasks = [t for t in self.tasks if t['category'] == filter_value]
        elif filter_type == 'priority':
            filtered_tasks = [t for t in self.tasks if t['priority'] == filter_value]
        else:
            filtered_tasks = self.tasks
        
        self.update_task_list(filtered_tasks)
        self.log_activity(f"Filtered tasks: {filter_type} {filter_value or ''}")
    
    def toggle_search(self):
        """Toggle the search bar visibility"""
        if self.search_frame.winfo_ismapped():
            self.search_frame.pack_forget()
            self.search_entry.delete(0, tk.END)
            self.update_task_list()
        else:
            self.search_frame.pack(fill=tk.X, pady=5)
            self.search_entry.focus()
    
    def perform_search(self):
        """Search tasks by title or description"""
        query = self.search_entry.get().lower()
        if query:
            filtered_tasks = [
                t for t in self.tasks 
                if query in t['title'].lower() or query in t['description'].lower()
            ]
            self.update_task_list(filtered_tasks)
            self.log_activity(f"Searched for: {query}")
    
    # ==============================================
    # Dialog Methods
    # ==============================================
    
    def open_add_task_dialog(self):
        """Open the add task dialog"""
        self.task_dialog = tk.Toplevel(self.root)
        self.task_dialog.title("➕ Add New Task")
        self.task_dialog.geometry("550x550")
        self.task_dialog.resizable(False, False)
        self.task_dialog.transient(self.root)
        self.task_dialog.grab_set()
        
        # Apply dark theme to dialog
        self.task_dialog.configure(bg=self.colors['dark_bg'])
        
        # Title
        ttk.Label(self.task_dialog, text="🌸 Add New Task", style='Title.TLabel').pack(pady=10)
        
        # Form frame
        form_frame = ttk.Frame(self.task_dialog, style='Light.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Task title
        ttk.Label(form_frame, text="Task Title:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        title_entry = ttk.Entry(form_frame, style='Dark.TEntry')
        title_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        desc_text = scrolledtext.ScrolledText(form_frame, 
                                           bg=self.colors['light_bg'],
                                           fg=self.colors['text'],
                                           insertbackground=self.colors['text'],
                                           wrap=tk.WORD,
                                           height=5)
        desc_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Due date
        ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        due_frame = ttk.Frame(form_frame, style='Light.TFrame')
        due_frame.pack(fill=tk.X, padx=5, pady=5)
        
        due_entry = ttk.Entry(due_frame, style='Dark.TEntry')
        due_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        cal_btn = ttk.Button(due_frame, text="📅", style='Secondary.TButton',
                            command=lambda: self.show_calendar(due_entry))
        cal_btn.pack(side=tk.RIGHT, padx=5)
        
        # Priority
        ttk.Label(form_frame, text="Priority:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        priority_combo = ttk.Combobox(form_frame, values=self.priorities, style='Dark.TCombobox')
        priority_combo.set("🔼 Medium")
        priority_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        category_combo = ttk.Combobox(form_frame, values=self.categories, style='Dark.TCombobox')
        category_combo.set("💼 Work")
        category_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(form_frame, style='Light.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                              command=self.task_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        add_btn = ttk.Button(button_frame, text="Add Task", style='Accent.TButton',
                           command=lambda: self.save_new_task(
                               title_entry.get(),
                               desc_text.get("1.0", tk.END).strip(),
                               due_entry.get(),
                               priority_combo.get(),
                               category_combo.get()
                           ))
        add_btn.pack(side=tk.RIGHT, padx=5, expand=True)
        
        # Set focus to title entry
        title_entry.focus()
    
    def save_new_task(self, title, description, due_date, priority, category):
        """Save a new task from the dialog"""
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty!", parent=self.task_dialog)
            return
        
        # Validate due date format
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Due date must be in YYYY-MM-DD format!", parent=self.task_dialog)
                return
        
        self.add_task(title, description, due_date, priority, category)
        self.task_dialog.destroy()
    
    def edit_selected_task(self):
        """Edit the currently selected task"""
        task = self.get_selected_task()
        if not task:
            messagebox.showwarning("Warning", "No task selected!", parent=self.root)
            return
        
        self.edit_dialog = tk.Toplevel(self.root)
        self.edit_dialog.title(f"✏️ Edit Task: {task['title']}")
        self.edit_dialog.geometry("500x550")
        self.edit_dialog.resizable(False, False)
        self.edit_dialog.transient(self.root)
        self.edit_dialog.grab_set()
        
        # Apply dark theme to dialog
        self.edit_dialog.configure(bg=self.colors['dark_bg'])
        
        # Main container with scrollbar
        container = ttk.Frame(self.edit_dialog, style='Dark.TFrame')
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container, bg=self.colors['dark_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Form frame
        form_frame = ttk.Frame(scrollable_frame, style='Light.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Task title
        ttk.Label(form_frame, text="Task Title:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.title_entry = ttk.Entry(form_frame, style='Dark.TEntry')
        self.title_entry.insert(0, task['title'])
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.desc_text = scrolledtext.ScrolledText(form_frame, 
                                                bg=self.colors['light_bg'],
                                                fg=self.colors['text'],
                                                insertbackground=self.colors['text'],
                                                wrap=tk.WORD,
                                                height=5)
        self.desc_text.insert("1.0", task['description'])
        self.desc_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Due date
        ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        due_frame = ttk.Frame(form_frame, style='Light.TFrame')
        due_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.due_entry = ttk.Entry(due_frame, style='Dark.TEntry')
        self.due_entry.insert(0, task['due_date'] if task['due_date'] else "")
        self.due_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        cal_btn = ttk.Button(due_frame, text="📅", style='Secondary.TButton',
                            command=lambda: self.show_calendar(self.due_entry))
        cal_btn.pack(side=tk.RIGHT, padx=5)
        
        # Priority
        ttk.Label(form_frame, text="Priority:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.priority_combo = ttk.Combobox(form_frame, values=self.priorities, style='Dark.TCombobox')
        self.priority_combo.set(task['priority'])
        self.priority_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.category_combo = ttk.Combobox(form_frame, values=self.categories, style='Dark.TCombobox')
        self.category_combo.set(task['category'])
        self.category_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Status (for board view)
        ttk.Label(form_frame, text="Status:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.status_combo = ttk.Combobox(form_frame, values=['todo', 'in_progress', 'done'], style='Dark.TCombobox')
        self.status_combo.set(task['status'])
        self.status_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Completion status
        self.completed_var = tk.BooleanVar(value=task['completed'])
        completed_check = ttk.Checkbutton(form_frame, 
                                        text="Completed",
                                        variable=self.completed_var,
                                        style='Dark.TCheckbutton')
        completed_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Button frame with only Save Changes button
        button_frame = ttk.Frame(form_frame, style='Light.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(button_frame, text="Save Changes", style='Accent.TButton',
                            command=self.save_edited_task)
        save_btn.pack(fill=tk.X, padx=5)
        
        # Set focus to title entry
        self.title_entry.focus()

    def save_edited_task(self):
        """Save changes from the edit dialog"""
        task = self.get_selected_task()
        if not task:
            return
            
        title = self.title_entry.get()
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty!", parent=self.edit_dialog)
            return
        
        due_date = self.due_entry.get()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Due date must be in YYYY-MM-DD format!", parent=self.edit_dialog)
                return
        
        self.edit_task(
            task['id'],
            title=title,
            description=self.desc_text.get("1.0", tk.END).strip(),
            due_date=due_date if due_date else None,
            priority=self.priority_combo.get(),
            category=self.category_combo.get(),
            status=self.status_combo.get(),
            completed=self.completed_var.get()
        )
        
        self.edit_dialog.destroy()
    
    def delete_selected_task(self):
        """Delete the currently selected task"""
        task = self.get_selected_task()
        if task:
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete '{task['title']}'?",
                                 parent=self.root):
                self.delete_task(task['id'])
        else:
            messagebox.showwarning("Warning", "No task selected!", parent=self.root)
    
    def quick_add_task(self):
        """Quickly add a task with minimal input"""
        self.quick_dialog = tk.Toplevel(self.root)
        self.quick_dialog.title("⚡ Quick Add Task")
        self.quick_dialog.geometry("400x150")
        self.quick_dialog.resizable(False, False)
        self.quick_dialog.transient(self.root)
        self.quick_dialog.grab_set()
        
        # Apply dark theme to dialog
        self.quick_dialog.configure(bg=self.colors['dark_bg'])
        
        # Title
        ttk.Label(self.quick_dialog, text="⚡ Quick Add Task", style='Title.TLabel').pack(pady=10)
        
        # Task title
        title_entry = ttk.Entry(self.quick_dialog, style='Dark.TEntry')
        title_entry.pack(fill=tk.X, padx=20, pady=5)
        title_entry.focus()
        
        # Button frame
        button_frame = ttk.Frame(self.quick_dialog, style='Light.TFrame')
        button_frame.pack(fill=tk.X, pady=10, padx=20)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", style='Secondary.TButton',
                              command=self.quick_dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, expand=True)
        
        add_btn = ttk.Button(button_frame, text="Add", style='Accent.TButton',
                           command=lambda: self.save_quick_task(title_entry.get()))
        add_btn.pack(side=tk.RIGHT, expand=True)
        
        # Bind Enter key to save
        title_entry.bind('<Return>', lambda e: self.save_quick_task(title_entry.get()))
    
    def save_quick_task(self, title):
        """Save a quick task"""
        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty!", parent=self.quick_dialog)
            return
        
        self.add_task(title)
        self.quick_dialog.destroy()
    
    def show_calendar(self, entry_widget):
        """Show a calendar for date selection"""
        from tkcalendar import Calendar
        
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.transient(self.root)
        top.grab_set()
        
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)
        
        def set_date():
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, cal.get_date())
            top.destroy()
        
        ttk.Button(top, text="OK", command=set_date, style='Accent.TButton').pack(pady=5)
    
    def show_stats(self):
        """Show detailed statistics"""
        stats_dialog = tk.Toplevel(self.root)
        stats_dialog.title("📊 Task Statistics")
        stats_dialog.geometry("600x500")
        stats_dialog.resizable(False, False)
        stats_dialog.transient(self.root)
        stats_dialog.grab_set()
        
        # Apply dark theme to dialog
        stats_dialog.configure(bg=self.colors['dark_bg'])
        
        # Title
        ttk.Label(stats_dialog, text="📊 Task Statistics", style='Title.TLabel').pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.Frame(stats_dialog, style='Light.TFrame')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Total tasks
        total_frame = ttk.Frame(stats_frame, style='Light.TFrame')
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text="Total Tasks:", style='Subtitle.TLabel').pack(side=tk.LEFT)
        ttk.Label(total_frame, text=str(len(self.tasks)), style='Subtitle.TLabel').pack(side=tk.RIGHT)
        
        # Completed tasks
        completed_frame = ttk.Frame(stats_frame, style='Light.TFrame')
        completed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(completed_frame, text="Completed Tasks:", style='Subtitle.TLabel').pack(side=tk.LEFT)
        completed_count = len([t for t in self.tasks if t['completed']])
        ttk.Label(completed_frame, text=f"{completed_count} ({completed_count/len(self.tasks)*100:.1f}%)", 
                 style='Subtitle.TLabel').pack(side=tk.RIGHT)
        
        # Tasks by priority
        ttk.Label(stats_frame, text="Tasks by Priority:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        for priority in self.priorities:
            prio_frame = ttk.Frame(stats_frame, style='Light.TFrame')
            prio_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(prio_frame, text=priority, style='Subtitle.TLabel').pack(side=tk.LEFT)
            
            tasks_in_priority = [t for t in self.tasks if t['priority'] == priority]
            completed_in_priority = len([t for t in tasks_in_priority if t['completed']])
            
            ttk.Label(prio_frame, 
                     text=f"{len(tasks_in_priority)} ({completed_in_priority} completed)", 
                     style='Subtitle.TLabel').pack(side=tk.RIGHT)
        
        # Tasks by category
        ttk.Label(stats_frame, text="Tasks by Category:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        for category in self.categories:
            cat_frame = ttk.Frame(stats_frame, style='Light.TFrame')
            cat_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(cat_frame, text=category, style='Subtitle.TLabel').pack(side=tk.LEFT)
            
            tasks_in_category = [t for t in self.tasks if t['category'] == category]
            completed_in_category = len([t for t in tasks_in_category if t['completed']])
            
            ttk.Label(cat_frame, 
                     text=f"{len(tasks_in_category)} ({completed_in_category} completed)", 
                     style='Subtitle.TLabel').pack(side=tk.RIGHT)
        
        # Close button
        ttk.Button(stats_frame, text="Close", style='Accent.TButton',
                  command=stats_dialog.destroy).pack(pady=10)
    
    def open_settings(self):
        """Open the settings dialog"""
        settings_dialog = tk.Toplevel(self.root)
        settings_dialog.title("⚙️ Settings")
        settings_dialog.geometry("500x400")
        settings_dialog.resizable(False, False)
        settings_dialog.transient(self.root)
        settings_dialog.grab_set()
        
        # Apply dark theme to dialog
        settings_dialog.configure(bg=self.colors['dark_bg'])
        
        # Title
        ttk.Label(settings_dialog, text="⚙️ Settings", style='Title.TLabel').pack(pady=10)
        
        # Notebook for settings tabs
        notebook = ttk.Notebook(settings_dialog, style='Dark.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Appearance tab
        appearance_frame = ttk.Frame(notebook, style='Light.TFrame')
        notebook.add(appearance_frame, text="🎨 Appearance")
        
        ttk.Label(appearance_frame, text="Theme Colors:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        # Color customization
        color_frame = ttk.Frame(appearance_frame, style='Light.TFrame')
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(color_frame, text="Dark Background", style='Secondary.TButton',
                  command=lambda: self.change_color('dark_bg')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(color_frame, text="Light Background", style='Secondary.TButton',
                  command=lambda: self.change_color('light_bg')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(color_frame, text="Accent Dark", style='Secondary.TButton',
                  command=lambda: self.change_color('accent_dark')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(color_frame, text="Accent Light", style='Secondary.TButton',
                  command=lambda: self.change_color('accent_light')).pack(side=tk.LEFT, padx=5)
        
        # Font settings
        ttk.Label(appearance_frame, text="Font:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        font_frame = ttk.Frame(appearance_frame, style='Light.TFrame')
        font_frame.pack(fill=tk.X, pady=5)
        
        self.font_var = tk.StringVar(value='Segoe UI')
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_var,
                                values=['Segoe UI', 'Arial', 'Helvetica', 'Times New Roman', 'Courier New'],
                                style='Dark.TCombobox')
        font_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(font_frame, text="Apply Font", style='Secondary.TButton',
                  command=self.apply_font).pack(side=tk.LEFT, padx=5)
        
        # Data tab
        data_frame = ttk.Frame(notebook, style='Light.TFrame')
        notebook.add(data_frame, text="💾 Data")
        
        ttk.Label(data_frame, text="Data Management:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
        
        ttk.Button(data_frame, text="Export Tasks", style='Secondary.TButton',
                  command=self.export_tasks).pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(data_frame, text="Import Tasks", style='Secondary.TButton',
                  command=self.import_tasks).pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(data_frame, text="Backup Data", style='Secondary.TButton',
                  command=self.backup_data).pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(data_frame, text="Reset All Data", style='Accent.TButton',
                  command=self.confirm_reset).pack(fill=tk.X, padx=20, pady=10)
        
        # About tab
        about_frame = ttk.Frame(notebook, style='Light.TFrame')
        notebook.add(about_frame, text="ℹ️ About")
        
        about_text = f"""🌸 Empress To-Do Manager 👑

Version: 1.0
Created with Python and Tkinter

Features:
- Multiple task views (list, board, calendar)
- Priority and category organization
- Progress tracking
- Customizable appearance

© {datetime.now().year} Empress Tools
"""
        
        about_label = ttk.Label(about_frame, text=about_text, style='Subtitle.TLabel', justify=tk.LEFT)
        about_label.pack(pady=20)
        
        ttk.Button(about_frame, text="Visit Website", style='Secondary.TButton',
                  command=lambda: webbrowser.open("https://example.com")).pack(pady=5)
        
        # Close button
        ttk.Button(settings_dialog, text="Close", style='Accent.TButton',
                  command=settings_dialog.destroy).pack(pady=10)
    
    def change_color(self, color_key):
        """Change a color in the theme"""
        color = askcolor(title=f"Choose {color_key.replace('_', ' ')} color",
                        initialcolor=self.colors[color_key])
        if color[1]:
            self.colors[color_key] = color[1]
            self.configure_styles()
            self.update_all_views()
    
    def apply_font(self):
        """Apply the selected font"""
        selected_font = self.font_var.get()
        try:
            # Update the base style
            self.style.configure('.', font=(selected_font, 10))
            
            # Update specific widgets that might need different font sizes
            self.style.configure('Title.TLabel', font=(selected_font, 18, 'bold'))
            self.style.configure('Subtitle.TLabel', font=(selected_font, 12))
            
            # Force refresh of all widgets
            self.update_all_views()
        except:
            messagebox.showerror("Error", "Failed to apply font. The font may not be available on your system.")
    
    def export_tasks(self):
        """Export tasks to a JSON file"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export tasks to file"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.tasks, f, indent=2)
                messagebox.showinfo("Success", "Tasks exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tasks: {str(e)}")
    
    def import_tasks(self):
        """Import tasks from a JSON file"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import tasks from file"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    imported_tasks = json.load(f)
                
                # Validate imported tasks
                if not isinstance(imported_tasks, list):
                    raise ValueError("Invalid file format")
                
                # Merge with existing tasks
                max_id = max([t['id'] for t in self.tasks]) if self.tasks else 0
                for task in imported_tasks:
                    if isinstance(task, dict) and 'title' in task:
                        max_id += 1
                        task['id'] = max_id
                        self.tasks.append(task)
                
                self.update_all_views()
                messagebox.showinfo("Success", f"Imported {len(imported_tasks)} tasks successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import tasks: {str(e)}")
    
    def backup_data(self):
        """Backup all application data"""
        backup_data = {
            'tasks': self.tasks,
            'categories': self.categories,
            'priorities': self.priorities,
            'colors': self.colors,
            'version': 1
        }
        
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".empressbak",
            filetypes=[("Empress Backup", "*.empressbak"), ("All files", "*.*")],
            title="Backup application data"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(backup_data, f, indent=2)
                messagebox.showinfo("Success", "Backup created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def confirm_reset(self):
        """Confirm before resetting all data"""
        if messagebox.askyesno("Confirm Reset", 
                             "Are you sure you want to reset all data? This cannot be undone!",
                             icon='warning'):
            self.tasks = []
            self.categories = ['💼 Work', '🏠 Personal', '🎓 Study', '❤️ Health', '🛒 Shopping', '🎉 Fun']
            self.priorities = ['🔥 Critical', '⚠️ High', '🔼 Medium', '🔽 Low', '🌱 Chill']
            
            self.update_all_views()
            messagebox.showinfo("Reset Complete", "All data has been reset to defaults.")
    
    def show_daily_quote(self):
        """Show a random motivational quote"""
        quotes = [
            "🌸 You got this, queen! Time to conquer your day!",
            "👑 Productivity is your superpower!",
            "✨ Small steps every day lead to big achievements!",
            "💖 You're capable of amazing things!",
            "🦋 Today is your day to shine!",
            "🍒 Organized mind, organized life!",
            "🎀 One task at a time - you've got this!",
            "💄 Make today so productive, tomorrow will be jealous!",
            "👠 The secret of getting ahead is getting started!",
            "👜 You're one task away from a better mood!"
        ]
        
        quote = random.choice(quotes)
        messagebox.showinfo("Daily Motivation", quote)
    
    # ==============================================
    # Data Persistence Methods
    # ==============================================
    
    def load_data(self):
        """Load saved data from file"""
        data_file = "empress_todo_data.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.categories = data.get('categories', self.categories)
                    self.priorities = data.get('priorities', self.priorities)
                    self.colors = data.get('colors', self.colors)
            except:
                # If loading fails, use defaults
                pass
    
    def save_data(self):
        """Save data to file"""
        data = {
            'tasks': self.tasks,
            'categories': self.categories,
            'priorities': self.priorities,
            'colors': self.colors
        }
        
        try:
            with open("empress_todo_data.json", 'w') as f:
                json.dump(data, f, indent=2)
        except:
            messagebox.showerror("Error", "Failed to save data!")
    
    # ==============================================
    # Event Handlers
    # ==============================================
    
    def on_task_selected(self, event):
        """Handle task selection event"""
        selected = self.get_selected_task()
        if selected:
            self.edit_task_btn.config(state=tk.NORMAL)
            self.delete_task_btn.config(state=tk.NORMAL)
            self.complete_task_btn.config(state=tk.NORMAL)
            
            # Update complete button text based on current state
            btn_text = "✓ Complete" if not selected['completed'] else "↻ Undo"
            self.complete_task_btn.config(text=btn_text)
        else:
            self.edit_task_btn.config(state=tk.DISABLED)
            self.delete_task_btn.config(state=tk.DISABLED)
            self.complete_task_btn.config(state=tk.DISABLED)
        
        self.update_status_bar()
    
    def on_tab_changed(self, event):
        """Handle notebook tab change event"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Board view
            self.update_board_view()
        elif current_tab == 2:  # Calendar view
            self.update_calendar_view()
        elif current_tab == 3:  # Progress view
            self.update_progress_view()
    
    def prev_month(self):
        """Navigate to previous month in calendar"""
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_calendar_view()
    
    def next_month(self):
        """Navigate to next month in calendar"""
        next_month = self.current_date.month % 12 + 1
        next_year = self.current_date.year + (1 if next_month == 1 else 0)
        self.current_date = self.current_date.replace(month=next_month, year=next_year, day=1)
        self.update_calendar_view()
    
    def log_activity(self, message):
        """Log activity to the activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_message = f"[{timestamp}] {message}\n"
        
        self.activity_log.configure(state='normal')
        self.activity_log.insert(tk.END, log_message)
        self.activity_log.configure(state='disabled')
        self.activity_log.see(tk.END)
    
    def on_closing(self):
        """Handle window closing event"""
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTodoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()