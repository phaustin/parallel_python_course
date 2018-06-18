* set .bash_profile so it reads .bashrc

    ```bash
    if [ -f ~/.bashrc ]; then
    source ~/.bashrc
    fi
    #
    # (https://perlgeek.de/en/article/set-up-a-clean-utf8-environment)
    #
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8

    echo "through bash profile"
    ```

* in your .bashrc, follow the anaconda suggestion to activate your base conda

    ```bash
    . /Users/phil/mb36/etc/profile.d/conda.sh
    conda activate root
    condap
    ```

where condap appears earlier in your .bashrc and looks like this:

    ```bash
    function condap()
     {
      #the_name=$(hostname) -- Linux, use next line for Macs
      the_name=$(scutil --get LocalHostName)
      out=`basename $CONDA_PREFIX`
      unset PS1
      PS1="\w ${out} \u@${the_name}\n% "
     }
    ```
    
this gives you a prompt that reminds you want conda environment you are in
If you activate a new environment you need to reexecute condap


