# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Also available under a BSD-style license. See LICENSE.

import torch

from torch_mlir_e2e_test.framework import TestUtils
from torch_mlir_e2e_test.registry import register_test_case
from torch_mlir_e2e_test.annotations import annotate_args, export

# ==============================================================================


class NllLossModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=0, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossModule())
def NllLossModule_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossStaticModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([2, 3], torch.float32, True),
            ([2], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=0, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossStaticModule())
def NllLossStaticModule_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossStaticModule_weight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([2, 3], torch.float32, True),
            ([2], torch.int64, True),
            ([3], torch.float32, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y, z):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=z, reduction=2, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossStaticModule_weight())
def NllLossStaticModule_weight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(2, 3), tu.randint(2, low=0, high=3), torch.tensor([0.3, 0.3, 0.4])
    )


class NllLossModule_mean(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=1, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossModule_mean())
def NllLossModule_mean_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossStaticModule_mean(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([2, 3], torch.float32, True),
            ([2], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=1, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossStaticModule_mean())
def NllLossStaticModule_mean_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossModule_sum(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=2, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossModule_sum())
def NllLossModule_sum_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossStaticModule_sum(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([2, 3], torch.float32, True),
            ([2], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=2, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossStaticModule_sum())
def NllLossStaticModule_sum_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossModule_1D(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([], torch.int64, True),
        ]
    )
    # Here the 2nd index is ignored.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=0, ignore_index=2
        )


@register_test_case(module_factory=lambda: NllLossModule_1D())
def NllLossModule_1D_basic(module, tu: TestUtils):
    module.forward(tu.rand(3), tu.randint(high=3))


class NllLossModule_ignore_index_out_of_bounds(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
        ]
    )
    # None of the index is ignored here, since the ignored index is out of bounds.
    def forward(self, x, y):
        return torch.ops.aten.nll_loss_forward(
            x, target=y, weight=None, reduction=0, ignore_index=10
        )


@register_test_case(module_factory=lambda: NllLossModule_ignore_index_out_of_bounds())
def NllLossModule_ignore_index_out_of_bounds_basic(module, tu: TestUtils):
    module.forward(tu.rand(2, 3), tu.randint(2, low=0, high=3))


class NllLossModule_backward(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=0,
            ignore_index=10,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward())
def NllLossModuleBackward_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(3), tu.rand(3, 4), torch.tensor([2, 3, 0]), torch.tensor(3.0)
    )


class NllLossModule_backwardWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=0,
            ignore_index=10,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backwardWeight())
def NllLossModuleBackwardWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(3),
        tu.rand(3, 4),
        torch.tensor([2, 3, 0]),
        tu.rand(4),
        torch.tensor(3.0),
    )


class NllLossModule_backward_ignore_index(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=0,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward_ignore_index())
def NllLossModuleBackward_ignore_index(module, tu: TestUtils):
    module.forward(
        tu.rand(3), tu.rand(3, 4), torch.tensor([2, 3, 0]), torch.tensor(3.0)
    )


class NllLossModule_backwardMean(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=1,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backwardMean())
def NllLossModuleBackwardMean_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1), tu.rand(3, 4), torch.tensor([2, 3, 0]), torch.tensor(3.0)
    )


class NllLossModule_backwardMeanWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=1,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backwardMeanWeight())
def NllLossModuleBackwardMeanWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1),
        tu.rand(3, 4),
        torch.tensor([2, 3, 0]),
        tu.rand(4),
        torch.tensor(3.0),
    )


class NllLossModule_backwardSum(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=2,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backwardSum())
def NllLossModuleBackwardSum_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1), tu.rand(3, 4), torch.tensor([2, 3, 0]), torch.tensor(3.0)
    )


class NllLossModule_backwardSumWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1, -1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=2,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backwardSumWeight())
def NllLossModuleBackwardSumWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1),
        tu.rand(3, 4),
        torch.tensor([2, 3, 0]),
        tu.rand(4),
        torch.tensor(3.0),
    )


class NllLossModule_backward1D(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=0,
            ignore_index=10,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1D())
def NllLossModuleBackward1D_basic(module, tu: TestUtils):
    module.forward(tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), torch.tensor(3.0))


class NllLossModule_backward1DWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=0,
            ignore_index=10,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1DWeight())
def NllLossModuleBackward1DWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), tu.rand(3), torch.tensor(3.0)
    )


class NllLossModule_backward1DMean(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=1,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1DMean())
def NllLossModuleBackward1DMean_basic(module, tu: TestUtils):
    module.forward(tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), torch.tensor(3.0))


class NllLossModule_backward1DMeanWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=1,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1DMeanWeight())
def NllLossModuleBackward1DMeanWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), tu.rand(3), torch.tensor(3.0)
    )


class NllLossModule_backward1DSum(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=None,
            reduction=2,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1DSum())
def NllLossModuleBackward1DSum_basic(module, tu: TestUtils):
    module.forward(tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), torch.tensor(3.0))


class NllLossModule_backward1DSumWeight(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1], torch.float32, True),
            ([-1], torch.float32, True),
            ([-1], torch.int64, True),
            ([-1], torch.float32, True),
            ([], torch.float32, True),
        ]
    )
    def forward(self, grad_output, input, target, weight, total_weight):
        return torch.ops.aten.nll_loss_backward(
            grad_output,
            input,
            target=target,
            weight=weight,
            reduction=2,
            ignore_index=1,
            total_weight=total_weight,
        )


@register_test_case(module_factory=lambda: NllLossModule_backward1DSumWeight())
def NllLossModuleBackward1DSumWeight_basic(module, tu: TestUtils):
    module.forward(
        tu.rand(1), tu.rand(3), torch.tensor([2, 3, 0]), tu.rand(3), torch.tensor(3.0)
    )


class PoissonNLLLossNoReductionModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [None, ([-1, -1], torch.float32, True), ([-1, -1], torch.float32, True)]
    )
    def forward(self, input, target):
        return torch.ops.aten.poisson_nll_loss(
            input=input,
            target=target,
            log_input=False,
            full=False,
            eps=1e-8,
            reduction=0,
        )


@register_test_case(module_factory=lambda: PoissonNLLLossNoReductionModule())
def PoissonNLLLossNoReductionModule_basic(
    module: PoissonNLLLossNoReductionModule, tu: TestUtils
):
    input = tu.rand(4, 3).abs()
    target = torch.poisson(input)
    module.forward(input, target)


class PoissonNLLLossMeanReductionModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [
            None,
            ([-1, -1], torch.float32, True),
            ([-1, -1], torch.float32, True),
        ]
    )
    def forward(self, input, target):
        return torch.ops.aten.poisson_nll_loss(
            input=input,
            target=target,
            log_input=True,
            full=False,
            eps=1e-8,
            reduction=1,
        )


@register_test_case(module_factory=lambda: PoissonNLLLossMeanReductionModule())
def PoissonNLLLossMeanReductionModule_basic(
    module: PoissonNLLLossMeanReductionModule, tu: TestUtils
):
    input = tu.rand(5, 7).abs()
    target = torch.poisson(input)
    module.forward(input, target)


class PoissonNLLLossSumReductionModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [None, ([-1, -1], torch.float32, True), ([-1, -1], torch.float32, True)]
    )
    def forward(self, input, target):
        return torch.ops.aten.poisson_nll_loss(
            input=input,
            target=target,
            log_input=True,
            full=False,
            eps=1e-8,
            reduction=2,
        )


@register_test_case(module_factory=lambda: PoissonNLLLossSumReductionModule())
def PoissonNLLLossSumReductionModule_basic(
    module: PoissonNLLLossSumReductionModule, tu: TestUtils
):
    input = tu.rand(3, 3)
    target = torch.poisson(input.abs())
    module.forward(input, target)


class PoissonNLLLossNonDefaultEpsModule(torch.nn.Module):
    def __init__(self):
        super().__init__()

    @export
    @annotate_args(
        [None, ([-1, -1], torch.float32, True), ([-1, -1], torch.float32, True)]
    )
    def forward(self, input, target):
        return torch.ops.aten.poisson_nll_loss(
            input=input,
            target=target,
            log_input=False,
            full=False,
            eps=0.5,
            reduction=1,
        )


@register_test_case(module_factory=lambda: PoissonNLLLossNonDefaultEpsModule())
def PoissonNLLLossNonDefaultEpsModule_basic(
    module: PoissonNLLLossNonDefaultEpsModule, tu: TestUtils
):
    input = tu.rand(5, 4)
    target = torch.poisson(input.abs())
    module.forward(input, target)
