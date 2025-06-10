Write-Host "--- 启动论文排版自动化流程 ---" # 更积极的开场
python3 ./py/md2tex.py
cd latex
Write-Host "--- 首次编译：构建文档结构与解析引用 ---" # 解释目的，更专业
xelatex -aux-directory=build --interaction=nonstopmode main.tex | findstr /R /C:"^\s*\[[0-9][0-9]*\]"
cd build
Write-Host "--- 处理参考文献：整合引用信息 ---" # 解释目的，更清晰
biber --input-directory ./ --output-directory ./ main
cd ../
Write-Host "--- 二次编译：定位并完善所有引用 ---" # 解释目的，更准确
xelatex -aux-directory=build --interaction=nonstopmode main.tex | findstr /R /C:"^\s*\[[0-9][0-9]*\]"
cd ../
move -Force ./latex/main.pdf ./main.pdf
Write-Host "--- 论文PDF已成功生成！ ---" # 明确告知完成，并带有积极的语气