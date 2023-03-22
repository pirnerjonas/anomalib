"""Unit Tests - Base Depth Datamodules."""

# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from anomalib.data import AnomalibDataModule
import pytest
from .test_datamodule import _TestAnomalibDataModule


class _TestAnomalibDepthDatamodule(_TestAnomalibDataModule):
    @pytest.mark.parametrize("subset", ["train", "val", "test"])
    def test_get_item_returns_correct_keys_and_shapes(self, datamodule: AnomalibDataModule, subset: str) -> None:
        """Test that the datamodule __getitem__ returns the correct keys and shapes."""

        # Get the dataloader.
        dataloader = getattr(datamodule, f"{subset}_dataloader")()

        # Get the first batch.
        batch = next(iter(dataloader))

        # Check that the batch has the correct keys.
        expected_keys = {"image_path", "depth_path", "label", "image", "depth_image"}

        if dataloader.dataset.task in ("detection", "segmentation"):
            expected_keys |= {"mask_path", "mask"}

            if dataloader.dataset.task == "detection":
                expected_keys |= {"boxes"}

        assert batch.keys() == expected_keys

        # Check that the batch has the correct shape.
        assert len(batch["image_path"]) == 4
        assert len(batch["depth_path"]) == 4
        assert batch["image"].shape == (4, 3, 256, 256)
        assert batch["depth_image"].shape == (4, 3, 256, 256)
        assert batch["label"].shape == (4,)

        # TODO: Detection task should return bounding boxes.
        # if dataloader.dataset.task == "detection":
        #     assert batch["boxes"].shape == (4, 4)

        if dataloader.dataset.task in ("detection", "segmentation"):
            assert batch["mask"].shape == (4, 256, 256)
