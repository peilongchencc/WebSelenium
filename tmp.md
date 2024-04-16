我使用的 selenium 4，我想要提取下列内容，代码应该怎么写呢？
```html
<div id="content_views" class="markdown_views prism-github-gist">
                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <p></p> 
<div class="toc"> 
 <h4><a name="t0"></a>文章目录</h4> 
 <ul><li><a href="#_4" rel="nofollow" target="_self">报错关键词</a></li><li><a href="#_10" rel="nofollow" target="_self">常见问题汇总及排查</a></li><li><ul><li><a href="#1__11" rel="nofollow" target="_self">1. 在脚本中使用相对导入</a></li></ul> 
  </li><li><a href="#_16" rel="nofollow" target="_self">详细解决方案</a></li><li><ul><li><a href="#1__17" rel="nofollow" target="_self">1. 【看这段基本够了】使用相对导入的时机</a></li><li><a href="#2__26" rel="nofollow" target="_self">2. 【扩展】如果你真的需要在包平级目录以外的位置调用包</a></li></ul> 
  </li><li><a href="#_35" rel="nofollow" target="_self">参考链接</a></li><li><a href="#__41" rel="nofollow" target="_self">* 扩展：名词解释</a></li><li><ul><li><a href="#script_43" rel="nofollow" target="_self">脚本（script）</a></li><li><a href="#module_45" rel="nofollow" target="_self">模块（module）</a></li><li><a href="#package_47" rel="nofollow" target="_self">包（package）</a></li><li><a href="#absolute_import_49" rel="nofollow" target="_self">绝对导入（absolute import）</a></li><li><a href="#relative_import_59" rel="nofollow" target="_self">相对导入（relative import）</a></li></ul> 
 </li></ul> 
</div> 
<p></p> 
<hr> 
<h2><a name="t1"></a><a id="_4"></a>报错关键词</h2> 
<ul><li><mark>相对导入（relative import）</mark>：报错<strong>模块</strong>（模块，区别于脚本<strong>不直接作为主程序运行</strong>，是一系列对象定义的集合）存在使用相对导入的包内模块调用关系，也即其中存在以 <code>.</code>（平级目录）或<code>..</code>（父级目录）起头的<code>import</code>语句。例如，<code>from .&lt;subpackage｜module&gt; import &lt;subpackage｜module｜func&gt;</code> 表示从<strong>报错模块平级目录的包或模块</strong>中调用嵌套的<strong>包或模块或函数</strong>。</li><li><mark>包（package）</mark>：利用<strong>文件夹组织的模块的集合</strong>，一般通过在各层级文件夹中放置<code>__init__.py</code>指示当前文件夹为一个<strong>包</strong>。</li><li><mark>无法识别的包文件（no known parent package）</mark>：当前 <strong>Python 解释器运行路径</strong>（<code>python path/to/main.py</code> 中 <code>python</code> 命令的执行位置）无法查找到当前执行脚本<strong>引用的包含相对导入的模块</strong>的最小包结构。</li></ul> 
<hr> 
<h2><a name="t2"></a><a id="_10"></a>常见问题汇总及排查</h2> 
<h3><a name="t3"></a><a id="1__11"></a>1. 在脚本中使用相对导入</h3> 
<p><mark>问题</mark>：相对导入是<strong>存在于包结构中，并在模块中使用</strong>的概念，而由 Python 解释器执行的程序是脚本文件，不应该存在相对导入。<br> <mark>解决方案</mark>：请使用绝对导入导入同级模块或包。若本地包文件存在于其它目录层级，考虑重新安排目录结构，或使用 <code>PYTHONPATH</code> 环境变量将本地包路径手动添加到 Python 解释器可识别包路径。详见文末扩展内容。</p> 
<hr> 
<h2><a name="t4"></a><a id="_16"></a>详细解决方案</h2> 
<h3><a name="t5"></a><a id="1__17"></a>1. 【看这段基本够了】使用相对导入的时机</h3> 
<blockquote> 
 <p>💡 你真的需要相对导入吗？如果你明确地知晓答案，也许就不应该出现这个问题。</p> 
</blockquote> 
<p>相对导入应当使用在<strong>包</strong>（由多个或多目录层级 <code>*.py</code> 模块组成）内模块中的 <code>import</code> 语句，用于<strong>内部模块功能之间的相互调用</strong>，而包内模块及功能则应当通过<strong>包外脚本调用</strong>。</p> 
<p>因此你应该这样思考和解决：<mark>当前的代码结构真的存在包-模块层级关系吗？如果存在，你应当在包外部通过脚本引用任意包-模块功能；如果不存在，你应当使用绝对导入直接导入同级目录模块。</mark></p> 
<h3><a name="t6"></a><a id="2__26"></a>2. 【扩展】如果你真的需要在包平级目录以外的位置调用包</h3> 
<p>当你意识到自己当前所处的位置确实为包外部，但尝试通过包平级目录以外的目录导入该包时，也可能遭遇导入问题。</p> 
<p>Python的默认包搜索路径为<code>sys.path</code>，一般指向当前Python环境pip默认安装包的目录。</p> 
<p>你可以通过<code>export PYTHONPATH=$PWD</code>快速添加当前目录（包所在目录）到搜索路径。如为开发中包项目，建议使用 <a href="https://github.com/direnv/direnv">direnv</a> 进行环境管理，如为长期依赖某些本地未发布的代码（包、模块）脚本文件，建议<a href="https://python3-cookbook.readthedocs.io/zh_CN/latest/c10/p09_add_directories_to_sys_path.html" rel="nofollow">通过代码添加</a>本地代码所在目录到<code>sys.path</code>。</p> 
<hr> 
<h2><a name="t7"></a><a id="_35"></a>参考链接</h2> 
<p><a href="https://stackoverflow.com/a/14132912/11533669" rel="nofollow">Stack Overflow: Relative imports for the billionth time</a><br> <a href="https://python3-cookbook.readthedocs.io/zh_CN/latest/c10/p09_add_directories_to_sys_path.html" rel="nofollow">python3-cookbook: 10.9 将文件夹加入到sys.path</a></p> 
<hr> 
<h2><a name="t8"></a><a id="__41"></a>* 扩展：名词解释</h2> 
<h3><a name="t9"></a><a id="script_43"></a>脚本（script）</h3> 
<p>通过执行该文件能够完成某项任务，其中存在必要的任务执行逻辑（一般通过 <code>if __name__ == '__main__:'</code> 代码块明确任务的整体执行逻辑），notebook 也可以列入这一范畴；</p> 
<h3><a name="t10"></a><a id="module_45"></a>模块（module）</h3> 
<p>Python 对象的集合，其内容为功能实现，目的是方便其它模块和脚本调用，因此不存在自身的运行逻辑（也即需要通过在其它文件中使用 <code>import</code> 语句调用，而非直接通过 <code>python module.py</code> 运行）；</p> 
<h3><a name="t11"></a><a id="package_47"></a>包（<a href="https://so.csdn.net/so/search?q=package&amp;spm=1001.2101.3001.7020" target="_blank" class="hl hl-1" data-report-view="{&quot;spm&quot;:&quot;1001.2101.3001.7020&quot;,&quot;dest&quot;:&quot;https://so.csdn.net/so/search?q=package&amp;spm=1001.2101.3001.7020&quot;,&quot;extra&quot;:&quot;{\&quot;searchword\&quot;:\&quot;package\&quot;}&quot;}" data-report-click="{&quot;spm&quot;:&quot;1001.2101.3001.7020&quot;,&quot;dest&quot;:&quot;https://so.csdn.net/so/search?q=package&amp;spm=1001.2101.3001.7020&quot;,&quot;extra&quot;:&quot;{\&quot;searchword\&quot;:\&quot;package\&quot;}&quot;}" data-tit="package" data-pretit="package">package</a>）</h3> 
<p>如果一个目录中存在多个模块，可以通过创建 <code>__init__.py</code> 文件将该当前目录标识为一个包。若多个模块放置于具有多层嵌套的目录当中，其逻辑关系为<strong>包（根目录）-&gt; 子包（子目录）-&gt; 模块（*.py）</strong>；</p> 
<h3><a name="t12"></a><a id="absolute_import_49"></a>绝对导入（absolute import）</h3> 
<p>从包/模块外部，按照目标模块的存在路径从外到内进行导入。绝对导入可以检索到三种来源的包：</p> 
<ol><li>Python自带或pip安装的包；</li><li>Python解释器启动位置同层模块和包；</li><li>人为添加到系统环境变量 <code>PYTHONPATH</code> 的模块和包。</li></ol> 
<p>绝对导入示例：</p> 
<ul><li>单独的模块：<code>import module</code>；</li><li>模块位于包内部（不存在子包）：<code>from package import module</code>；</li><li>模块位于包内部（存在子包）：<code>from package.subpackage import module</code>）。</li></ul> 
<h3><a name="t13"></a><a id="relative_import_59"></a>相对导入（relative import）</h3> 
<p>位于同一包中的不同子包和模块，可以通过前缀<code>.</code>标识存在调用关系的包/模块之间的路径依赖关系并进行相对调用。示例：</p> 
<ul><li>同层目录的模块：<code>from . import module</code>；</li><li>模块位于同层包内部（不存在子包）：<code>from .package import module</code>；</li><li>模块位于同层包内部（存在子包）：<code>from .packge.subpackge import module</code>；</li><li>模块位于上一层级目录：将以上语句的前缀进行替换 <code>from . -&gt; from ..</code>，以此类推。</li></ul>
                </div>
```

"content_views"