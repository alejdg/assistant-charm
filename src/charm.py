#!/usr/bin/env python3
# Copyright 2024 Alexandre
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops

logger = logging.getLogger(__name__)


class CharmAssistantCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _actions_is_list(self, actions):
        return isinstance(actions, list)

    def _action_is_dict(self, action):
        return isinstance(action, dict)

    def _valid_actions_struct(self, actions):
        for action in actions:
            if "name" not in action or "cmd" not in action:
                return False
        return True

    def _valid_actions(self, actions):
        """
        Validates the actions list.

        Args:
            actions (list): The list of actions to validate.

        Returns:
            bool: True, False.
        """
        if not self._actions_is_list(actions):
            return False

        # Each action must be a dictionary and follow our structure
        for action in actions:
            if not self._action_is_dict(action):
                return False
            if not self._valid_actions_struct(action):
                return False
        return True


if __name__ == "__main__":  # pragma: nocover
    ops.main(CharmAssistantCharm)  # type: ignore
