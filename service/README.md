# OpenShift configuration with Kustomize

Resource configuration and secret consumption for OpenShift projects are managed
using [`kustomize`](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/).

## Important note

`officehours-qa` was renamed to `officehours-test` during the migration process to ROSA. Not everything has been renamed yet, including the domain names and some of the directory names here. Just know that these instances are currently identical. 

## Setup

1. Populate `service/base/secret/*` and `service/overlays/*/secret/*`.

    Sensitive values and files are located in the
    [Office Hours Secrets](https://www.dropbox.com/sh/n1igrgdsm4rt4uf/AAAXLbZOT7tpVk8XZEQj5E0ca?dl=0)
    Dropbox folder. Merge the `base` and `overlays` directories with their equivalents in the `service`
    directory in your local repository.

    1. Download `base.zip`: https://www.dropbox.com/scl/fo/ibafd6hctx55ezcaa5dof/h?rlkey=qv53e05fu1z9w0h8vire7cqjk&dl=1
    1. Extract `base.zip`: `(cd service/base; unzip base.zip)`
    1. Download `overlays.zip`: https://www.dropbox.com/scl/fo/9q8mvuezmvmw7524veshx/h?rlkey=gds439f8vb2531gkih221giqh&dl=1
    1. Extract `overlays.zip`: `(cd service/overlays; unzip overlays.zip)`

2. Install `kustomize`.

    You can install Kustomize using homebrew or using the command from the
    [website](https://kubectl.docs.kubernetes.io/installation/kustomize/binaries/),
    and adding version 5.1.0 (what is tested/supported for now) as an argument.
    ```
    curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash -s 5.1.0
    ```

## Updating a project

1. Login and select the desired project using `oc`.
    ```
    oc login ...
    oc project officehours-dev
    ```

2. Fron the `service` directory, use `kustomize build` on an overlay directory 
and pipe the result to `oc apply`.
    ```
    kustomize build overlays/dev | oc apply -f - --validate
    ```

To make changes to a project's ingress (e.g. updating certificates),
you may need to first delete the ingress before running `kustomize build`.
```
oc delete ingress some-ingress-name
```

## Split kustomize output into files

For debugging purposes, it may be helpful to get the output from `kustomize`
as individual files, one for each artifact.  This can be done by splitting the
output into files and then giving those files meaningful names.

### Using the provided script

The `service/out/run.sh` script can be used to run Kustomize and the commands
to split its output and rename the files.  To run the script, use the
following commands:

```sh
cd service/out
./run.sh
```

The script will make multiple YAML files in the `out` directory corresponding
to the artifacts that `kustomize` generates.  The files will be named
according to the kind of artifact and its internal name.

### Manual steps

Using `gcsplit`, installed via Homebrew `coreutils` package, an asterisk
indicates splitting as many times as necessary

```sh
kustomize build overlays/prod | gcsplit -s - /^---$/ '{*}'
```

If using `csplit` included with macOS, it may be necessary to adjust the
number of splits (7)…

```sh
kustomize build overlays/prod | csplit -s - /^---$/ '{7}'
```

Finally, rename the `xx` files created by `csplit` with meaningful names.  In
this case, name the files for the kind of artifact and its internal name.  Use
`yq` (may be installed via Homebrew) to query values from YAML files…

```sh
for i in xx*; do sed '/^---$/,1d' $i > $(yq '.kind + "-" + .metadata.name + ".yaml"' $i); done; rm xx*
```

