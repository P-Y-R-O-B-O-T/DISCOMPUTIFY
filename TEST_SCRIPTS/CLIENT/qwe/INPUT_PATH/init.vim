call plug#begin('~/.config/nvim/plugged')
Plug 'navarasu/onedark.nvim'
Plug 'nvim-lualine/lualine.nvim'
Plug 'kyazdani42/nvim-web-devicons'
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'kyazdani42/nvim-tree.lua'
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim', { 'tag': '0.1.0' }
Plug 'nvim-telescope/telescope.nvim', { 'rev': '0.1.x' }
Plug 'folke/which-key.nvim'
Plug 'akinsho/bufferline.nvim', { 'tag': 'v2.*' }
call plug#end()

lua << END
require('onedark').setup  {
	-- Main options --
	style = 'deep', -- Default theme style. Choose between 'dark', 'darker', 'cool', 'deep', 'warm', 'warmer' and 'light'
	transparent = true,  -- Show/hide background
	term_colors = true, -- Change terminal color as per the selected theme style
	ending_tildes = true, -- Show the end-of-buffer tildes. By default they are hidden
	cmp_itemkind_reverse = false, -- reverse item kind highlights in cmp menu

	-- Change code style ---
	-- Options are italic, bold, underline, none
	-- You can configure multiple style with comma seperated, For e.g., keywords = 'italic,bold'
	code_style = {
		comments = 'italic',
		keywords = 'none',
		functions = 'none',
		strings = 'none',
		variables = 'bold'
	},

	-- Custom Highlights --
	colors = {}, -- Override default colors
	highlights = {}, -- Override highlight groups

	-- Plugins Config --
	diagnostics = {
		deep = true,      -- deep colors for diagnostic
		undercurl = true,   -- use undercurl instead of underline for diagnostics
		background = true,    -- use background color for virtual text
	},
}
END

lua << END
require('lualine').setup {
	options = {
		icons_enabled = true,
		theme = 'auto',
		component_separators = { left = '', right = ''},
		section_separators = { left = '', right = ''},
		disabled_filetypes = {
			statusline = {},
			winbar = {},
		},
		ignore_focus = {},
		always_divide_middle = true,
		globalstatus = false,
		refresh = {
			statusline = 1000,
			tabline = 1000,
			winbar = 1000,
		}
	},
	sections = {
		lualine_a = {'mode'},
		--lualine_b = {'branch', 'diff', 'diagnostics'},
		lualine_b = {'branch', 'diff'},
		lualine_c = {'filename'},
		lualine_x = {'encoding', 'fileformat', 'filetype'},
		lualine_y = {'progress'},
		lualine_z = {'location'}
	},
	inactive_sections = {
		lualine_a = {},
		lualine_b = {},
		lualine_c = {'filename'},
		lualine_x = {'location'},
		lualine_y = {},
		lualine_z = {}
	},
	tabline = {},
	winbar = {},
	inactive_winbar = {},
	extensions = {}
}
END

lua << END
require('nvim-treesitter.configs').setup {
	highlight = {
		enable = true,
		-- Setting this to true will run `:h syntax` and tree-sitter at the same time.
		-- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
		-- Using this option may slow down your editor, and you may see some duplicate highlights.
		-- Instead of true it can also be a list of languages
		additional_vim_regex_highlighting = true,
	},
}
END

lua << END
require('nvim-tree').setup()
END

lua << END
require('telescope').setup{
	defaults = {
		-- Default configuration for telescope goes here:
		-- config_key = value,
		mappings = {
			i = {
			-- map actions.which_key to <C-h> (default: <C-/>)
			-- actions.which_key shows the mappings for your picker,
			-- e.g. git_{create, delete, ...}_branch for the git_branches picker
			['<C-h>'] = 'which_key'
			}
		}
	},
	pickers = {
		-- Default configuration for builtin pickers goes here:
		-- picker_name = {
		--   picker_config_key = value,
		--   ...
		-- }
		-- Now the picker_config_key will be applied every time you call this
		-- builtin picker
	},
	extensions = {
		-- Your extension configuration goes here:
		-- extension_name = {
		--   extension_config_key = value,
		-- }
		-- please take a look at the readme of the extension you want to configure
	}
}
END

lua << EOF
require('which-key').setup {
	-- your configuration comes here
	-- or leave it empty to use the default settings
	-- refer to the configuration section below
}
EOF

lua << END
require("bufferline").setup {
	options = {
		buffer_close_icon = '',
        close_icon = ''
	}
}
END

colorscheme onedark

:set ts=4
:set sw=4
:set autoindent
:set number
:set nowrap
:set mouse=

map <A-Left> :bp<CR>
map <A-Right> :bn<CR>
map <A-Up> :NvimTreeOpen<CR>
map <A-Down> :NvimTreeClose<CR>
map <A-f> :Telescope<Space>find_files<CR>
map <A-w> :WhichKey<CR>
