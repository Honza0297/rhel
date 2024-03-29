from leapp.actors import Actor
from leapp.libraries.actor.scanner import detect_config_error
from leapp.models import GrubConfigError
from leapp.reporting import Report, create_report
from leapp import reporting
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class DetectGrubConfigError(Actor):
    """
    Check grub configuration for syntax error in GRUB_CMDLINE_LINUX value.
    """

    name = 'detect_grub_config_error'
    consumes = ()
    produces = (Report, GrubConfigError)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        config = '/etc/default/grub'
        error_detected = detect_config_error(config)
        if error_detected:
            create_report([
                reporting.Title('Syntax error detected in grub configuration'),
                reporting.Summary(
                    'Syntax error was detected in GRUB_CMDLINE_LINUX value of grub configuration. '
                    'This error is causing booting and other issues. '
                    'Error is automatically fixed by add_upgrade_boot_entry actor.'
                ),
                reporting.Severity(reporting.Severity.LOW),
                reporting.Tags([reporting.Tags.BOOT]),
                reporting.RelatedResource('file', config)
            ])

        self.produce(GrubConfigError(error_detected=error_detected))
