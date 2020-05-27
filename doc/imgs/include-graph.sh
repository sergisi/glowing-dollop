 for i in `seq 13 20`;do
   echo "\begin{figure}[H] \centering; \includegraphics[width=10cm]{imgs/histogram-$i.png}; \label{fig:hist-$i}; \caption{Histogram of Zipf Distribution using s=$i} \end{figure}";
   done;